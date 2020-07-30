import patchParser as parse
import test_match as match
import slice_and_parse as slice
import diff_match_patch as dmp_module
import re
from enum import Enum

class ContextResult:
    """
    Context_Result stores the fields that determine
        whether the patch needs to be applied or not

    run_patch: Boolean that determines if the patch 
        should still be applied

    message: Is a string that describes the output 
        of the context related changes 
    """

    def __init__(self, status, messages):
        self.status = status
        self.messages = messages

class CONTEXT_DECISION(Enum):
    DONT_RUN = 0
    RUN = 1

def context_changes(patch_file_path):
    """
    context_changes(str): takes in a patch file path and 
        returns a ContextResult object that determines 
        weather to run the patch or not and an associate 
        message that can be shown to users

    patch_file_path: string representing the path to a patch file
    """
    context_result_list = []

    patch_file = parse.PatchFile(patch_file_path)
    patch_file.getPatch()

    for patch in patch_file.patches:
        file_name = patch.getFileName()
        # TODO: update this to not be hardcoded
        file_path = f"../../../msm-3.10{file_name}"

        file_slice = slice.SliceParser(file_path)
        file_slice_parsed = file_slice.slice_parse()

        # TODO: find optimal retry object 
        # (maybe do 3 runs while expanding scope)
        diff_file_patch = match.find_diffs(
            patch,
            file_path,
            try_already_applied=True,
            retry_obj=match.Retry(3, 100),
        )

        if diff_file_patch.match_status != match.Diff.MatchStatus.MATCH_FOUND:
            context_result = ContextResult(CONTEXT_DECISION.DONT_RUN.value, 
                [f"A context match was not found."])
            context_result_list.append([context_result])
            continue
        
        if not diff_file_patch.context_diffs:
            context_result = ContextResult(CONTEXT_DECISION.DONT_RUN.value, 
                [f"No context related issues found."])
            context_result_list.append([context_result])
            continue
            
        context_diffs_list = []
        for context_diff in diff_file_patch.context_diffs:
            if context_diff.match_ratio < match.LEVENSHTEIN_RATIO:
                output_message = ("The match ratio between the source and patch code was low. "
                    f"We received a match ratio of {context_diff.match_ratio}, expected a ratio" 
                    f" greater than or equal to {match.LEVENSHTEIN_RATIO}.")
            
                context_result = ContextResult(CONTEXT_DECISION.DONT_RUN.value, [output_message])
                context_diffs_list.append(context_result)
                continue

            if re.search('^(\w+( )?){2,}\([^!@#$+%^]+?\)', context_diff.file_line):
                output_message = (f"We noticed a context-related difference between the function"
                    f" in the source code [{context_diff.file_line}] We are suggesting to replace"
                    f" this function with [{context_diff.patch_line}]")
                # TODO: should we give information from the slicer here? 
                # TODO: should this be a false?
                context_result = ContextResult(CONTEXT_DECISION.DONT_RUN.value, [output_message])
                context_diffs_list.append(context_result)
                continue
                
            diff_match = dmp_module.diff_match_patch()
            line_patch_diffs = diff_match.diff_main(
                    context_diff.file_line, context_diff.patch_line
            )

            if not line_patch_diffs:
                context_result = ContextResult(CONTEXT_DECISION.RUN.value, 
                    ["We have found a match, run the patch."])
                context_diffs_list.append(context_result)
                continue
            
            print(line_patch_diffs)
            function_name = context_diff.function_for_patch
            output_messages = []
            for line_diff in line_patch_diffs:
                if line_diff[0] == 0 and line_diff[1].rstrip().endswith("="):
                    output_messages.append("An R-Value has been changed, the slicer does not have" 
                        " information about R-Value variables.")
                
                elif line_diff[0] == 0 and line_diff[1].rstrip().startswith("="):
                    if function_name:
                        function_name = function_name.split("(")[0].split()[-1]
                        file_var = [
                            item for item in line_patch_diffs if item[0] == -1
                        ][0]

                        var_information = file_slice_parsed[function_name][file_var]
                        output_messages.append(f"L-Value change, User should consider the following"
                            f" slicer_output: {var_information})")
                    else:
                        output_messages.append("L-Value change but function name was not supplied by"
                            " matching code, we can not provide slicer information")

            if not output_messages:
                output_messages.append("Context difference was neither an L-Value or R-Value change.")
            
            context_result = ContextResult(CONTEXT_DECISION.RUN.value, output_messages)
            context_diffs_list.append(context_result)
        
        context_result_list.append(context_diffs_list)
        
    return context_result_list
    