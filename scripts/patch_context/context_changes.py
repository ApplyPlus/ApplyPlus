import scripts.patch_apply.patchParser as parse
import scripts.patch_match.test_match as match
import scripts.patch_context.slice_and_parse as slice
import diff_match_patch as dmp_module
import re
from scripts.enums import CONTEXT_DECISION, MatchStatus


class ContextResult:
    """
    Context_Result stores the fields that determine
        whether the patch needs to be applied or not

    run_patch: Boolean that determines if the patch
        should still be applied

    message: Is a string that describes the output
        of the context related changes

    is_comment: Boolean that determines if the additional
        lines are comments or not
    """

    def __init__(self, status, messages, diff_obj, is_comment):
        self.status = status
        self.messages = messages
        self.diff_obj = diff_obj
        self.is_comment = is_comment


def context_changes(sub_patch, expand=False):
    """
    context_changes(str): takes in a sub-patch and
        returns a ContextResult object that determines
        whether to run the patch or not and an associate
        message that can be shown to users

    patch_file_path: string representing the path to a patch file
    """

    file_name = sub_patch.getFileName()

    # TODO: update this to not be hardcoded
    file_path = f"../msm-3.10{file_name}"

    file_slice = slice.SliceParser(file_path)
    file_slice_parsed = file_slice.slice_parse()

    if not file_slice_parsed:
        return ContextResult(
            CONTEXT_DECISION.DONT_RUN.value,
            "The extension of the file the patch refers to is not supported by srcML",
            None,
            False,
        )

    # TODO: find optimal retry object
    # (maybe do 3 runs while expanding scope)
    if expand:
        diff_file_patch = match.find_diffs(
            sub_patch,
            file_path,
            retry_obj=match.Retry(1000, 50),
        )
    else:
        diff_file_patch = match.find_diffs(
            sub_patch,
            file_path,
            retry_obj=match.Retry(5, 50),
        )

    if diff_file_patch.match_status != MatchStatus.MATCH_FOUND:
        context_result = ContextResult(
            CONTEXT_DECISION.DONT_RUN.value,
            "A context match was not found.",
            diff_file_patch,
            False,
        )

        return context_result

    if not diff_file_patch.context_diffs:
        context_result = ContextResult(
            CONTEXT_DECISION.RUN.value,
            "No context related issues found.",
            diff_file_patch,
            False,
        )

        return context_result

    apply_patch = True
    comment_line = True
    line_concat = ""
    output_message = ""

    for context_diff in diff_file_patch.context_diffs:

        if context_diff.match_ratio < match.LEVENSHTEIN_RATIO:
            output_message = (
                f"For the context line difference in the patch file {context_diff.patch_line}"
                f" and in the source file {context_diff.file_line} the match ratio {context_diff.match_ratio}"
                f" is below the threashold match ratio of {match.LEVENSHTEIN_RATIO}. For this reason, we recommend"
                f" to not run this patch."
            )

            context_result = ContextResult(
                CONTEXT_DECISION.DONT_RUN.value,
                output_message,
                diff_file_patch,
                False,
            )

            return context_result

        rhs_function_call_reg = re.search(
            "=( ?)(\w+( )?){2,}\([^!@#$+%^]+?\)", context_diff.file_line
        )
        lhs_function_call_reg = re.search(
            "( +)(\w+( )?)\([^!@#$+%^]+?\)", context_diff.file_line
        )
        function_definition_reg = re.search(
            "(\w+( )?){0,3}\([^!@#$+%^]+?\)", context_diff.file_line
        )

        if rhs_function_call_reg:
            output_message = (
                f"For the context line difference in the patch file {context_diff.patch_line}"
                f" and in the source file {context_diff.file_line} represents a function call on the"
                f" RHS of an expression. Since this the value on the LHS of the expression may have "
                f" dependencies at other locations in the file, we recommend to not run this patch."
            )

            context_result = ContextResult(
                CONTEXT_DECISION.DONT_RUN.value,
                output_message,
                diff_file_patch,
                False,
            )

            return context_result

        # A function call is being made while not being assigned to a variable
        # we will continue with running the patch for this case
        elif lhs_function_call_reg and lhs_function_call_reg.group() == context_diff.file_line:
            continue

        elif function_definition_reg:
            output_message = (
                f"For the context line difference in the patch file {context_diff.patch_line}"
                f" and in the source file {context_diff.file_line} represents a function definition."
                f" Since the previous function defintion in the source file may have dependencies at "
                f" other areas in the code base, we recommend to not run this patch."
            )

            context_result = ContextResult(
                CONTEXT_DECISION.DONT_RUN.value, output_message, diff_file_patch, False
            )

            return context_result

        diff_match = dmp_module.diff_match_patch()
        line_patch_diffs = diff_match.diff_main(
            context_diff.file_line, context_diff.patch_line
        )

        unchanged_diff_list = [
            item[1] for item in line_patch_diffs if item[0] == 0 and "=" in item[1]
        ]

        if not unchanged_diff_list:
            output_message = (
                f"For the context line difference in the patch file {context_diff.patch_line}"
                f" and in the source file {context_diff.file_line} represents neither a function"
                f"definition, function call, L-Value, or R-Value change."
                f" For this reason we recommend to not run this patch. "
            )

            context_result = ContextResult(
                CONTEXT_DECISION.DONT_RUN.value, output_message, diff_file_patch, False
            )

            return context_result

        else:
            unchanged_diff = unchanged_diff_list[0]

            if unchanged_diff.rstrip().startswith("="):
                output_message = (
                    f"For the context line difference in the patch file {context_diff.patch_line}"
                    f" and in the source file {context_diff.file_line} represents an L-Value change."
                    f" For this reason we recommend to not run this patch. "
                )

                context_result = ContextResult(
                    CONTEXT_DECISION.DONT_RUN.value,
                    output_message,
                    diff_file_patch,
                    False,
                )

                return context_result

            elif unchanged_diff.rstrip().endswith("="):
                # dissect the context line to determine type
                function_name = context_diff.function_for_patch
                potential_file_var = [
                    item for item in line_patch_diffs if item[0] == -1
                ][0]

                if function_name:
                    function_name = function_name.split("(")[0].split()[-1]
                    try:
                        var_information = file_slice_parsed[function_name][file_var]
                    except:
                        var_information = None

                    # L-Value change on the RHS of exprsession
                    if var_information:
                        output_message = (
                            f"For the context line difference in the patch file {context_diff.patch_line}"
                            f" and in the source file {context_diff.file_line} represents an L-Value change."
                            f" For this reason we recommend to not run this patch. "
                        )

                        context_result = ContextResult(
                            CONTEXT_DECISION.DONT_RUN.value,
                            output_message,
                            diff_file_patch,
                            False,
                        )

                        return context_result
                    else:
                        # R-Value change we continue with running the patch
                        continue
                else:
                    # we don't know the function name
                    is_var = False
                    for _, value in file_slice_parsed.items():
                        for var_name, _ in value.items():
                            if var_name == potential_file_var:
                                is_var = True

                    if is_var:
                        output_message = (
                            f"For the context line difference in the patch file {context_diff.patch_line}"
                            f" and in the source file {context_diff.file_line} represents an L-Value change."
                            f" For this reason we recommend to not run this patch. "
                        )

                        context_result = ContextResult(
                            CONTEXT_DECISION.DONT_RUN.value,
                            output_message,
                            diff_file_patch,
                            False,
                        )

                        return context_result
                    else:
                        # R-Value
                        continue

    if diff_file_patch.additional_lines:
        for add_lines in diff_file_patch.additional_lines:
            line_concat += add_lines
            # To match a single line comment.
            if re.search("^[\/\/]+.*", add_lines):
                comment_line &= True
            else:
                comment_line &= False

        # To match a multi-line comment.
        if re.search("\/\*(\*(?!\/)|[^*])*\*\/", line_concat):
            comment_line = True
        else:
            comment_line = False
    else:
        comment_line = False

    return ContextResult(
        True, "This Patch can be applied.", diff_file_patch, comment_line
    )
