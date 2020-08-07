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

def context_changes(sub_patch):
    """
    context_changes(str): takes in a sub-patch and 
        returns a ContextResult object that determines 
        whether to run the patch or not and an associate 
        message that can be shown to users

    patch_file_path: string representing the path to a patch file
    """

    file_name = sub_patch.getFileName()

    # TODO: update this to not be hardcoded
    file_path = f"../../../msm-3.10{file_name}"

    file_slice = slice.SliceParser(file_path)
    file_slice_parsed = file_slice.slice_parse()

    # TODO: find optimal retry object
    # (maybe do 3 runs while expanding scope)
    diff_file_patch = match.find_diffs(
        sub_patch,
        file_path,
        retry_obj=match.Retry(3, 100),
    )

    if diff_file_patch.match_status != match.Diff.MatchStatus.MATCH_FOUND:
        context_result = ContextResult(CONTEXT_DECISION.DONT_RUN.value, 
            "A context match was not found.")
        
        return context_result
        
    
    if not diff_file_patch.context_diffs:
        context_result = ContextResult(CONTEXT_DECISION.RUN.value, 
            "No context related issues found.")
        
        return context_result
        
    apply_patch = True
    output_message = ""
    context_diff_count = 1
    
    for context_diff in diff_file_patch.context_diffs:
        if context_diff.match_ratio < match.LEVENSHTEIN_RATIO:
            output_message += (f"Context Diff #{context_diff_count}: The match ratio between the source and patch code was low. " 
                f"We received a match ratio of {context_diff.match_ratio}, expected a ratio greater than or equal to {match.LEVENSHTEIN_RATIO}. " 
                f"The patch line was {context_diff.patch_line} whereas the file line was {context_diff.file_line}\n")
                
            apply_patch &= CONTEXT_DECISION.DONT_RUN.value
            context_diff_count += 1
            continue

        elif re.search('^(\w+( )?){2,}\([^!@#$+%^]+?\)', context_diff.file_line):
            output_message += (f"Context Diff #{context_diff_count}: We noticed a context-related difference between the "
                f"function in the source code [{context_diff.file_line}] We are suggesting to replace this function with [{context_diff.patch_line}]\n")
            
            # TODO: should we give information from the slicer here? 
            # TODO: should this be a false?
            
            apply_patch &= CONTEXT_DECISION.DONT_RUN.value
            context_diff_count += 1
            continue
        
        diff_match = dmp_module.diff_match_patch()
        line_patch_diffs = diff_match.diff_main(
                context_diff.file_line, context_diff.patch_line
        )
        
        # TODO: verify if this line runs
        if not line_patch_diffs:
            apply_patch &= CONTEXT_DECISION.RUN.value

        # dissect the context line to determine type        
        function_name = context_diff.function_for_patch
        for line_diff in line_patch_diffs:
            if line_diff[0] == 0 and line_diff[1].rstrip().endswith("="):
                output_message += (f"Context Diff #{context_diff_count}: An L-Value has been changed, we will not apply the patch.\n")
                apply_patch &= CONTEXT_DECISION.DONT_RUN.value
                break

            elif line_diff[0] == 0 and line_diff[1].rstrip().startswith("="):
                if function_name:
                    function_name = function_name.split("(")[0].split()[-1]
                    file_var = [
                            item for item in line_patch_diffs if item[0] == -1
                    ][0]

                    var_information = file_slice_parsed[function_name][file_var]
                    output_message += f"Context Diff #{context_diff_count}: R-Value change, User should consider the following slicer_output: {var_information}"
                    apply_patch &= CONTEXT_DECISION.RUN.value

                    
                else:
                    output_message += (f"Context Diff #{context_diff_count}: R-Value change but function name was not " 
                        f"supplied by matching code, we can not provide slicer information\n")
                    apply_patch &= CONTEXT_DECISION.RUN.value

                break
        
        context_diff_count += 1
        
    return ContextResult(apply_patch, output_message)
