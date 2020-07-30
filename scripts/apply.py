import argparse

import patchParser as parse
# import check_file_exists_elsewhere as fileCheck
import test_match as tm
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reverse", help="Apply a patch in reverse files and/or to the index.", action='store_true')

    parser.add_argument(
        'pathToPatch', help="Path to the patch that needs to be applied.")

    args = parser.parse_args()
    return args

def apply_reverse(pathToPatch):
    print ("Apply in reverse called")

def are_context_changes_important(diff_obj):
    return False

def apply(pathToPatch):
    print("apply called")
    patch_file = parse.PatchFile(pathToPatch)
    patch_file.runPatch()
    if(patch_file.runSuccess == True):
        print("Successfully applied")
        return 0
    else:
        print("Patch failed with error:")
        error_message = patch_file.runResult.decode('utf-8')
        print(error_message)

        error_message_lines = error_message.split('\n')        
        already_exists = set()
        file_not_found = set()
        does_not_apply = set()

        for line in error_message_lines:
            split_line = line.split(":")
            if "patch does not apply" in line:
                does_not_apply.add(split_line[1].strip())
            elif "already exists" in line:
                already_exists.add(split_line[1].strip())
            elif "No such file" in line:
                file_not_found.add(split_line[1].strip())
        
        patch_file.getPatch()
        
        # TODO: Handle file that already exists
        # TODO: Handle the not found files once functions to handle that have been merged

        # Handling sub patches do not apply
        try_subpatches = input("Would you like to try and apply subpatches? [Y/n] ")
        if try_subpatches.upper() == "Y":
            successful_subpatches = []
            failed_subpatches_with_matched_code = []
            subpatches_without_matched_code = []
            for patch in patch_file.patches:
                # [1:] is used to remove the leading slash
                fileName = patch._fileName[1:]
                if fileName in does_not_apply:
                    subpatch_name =  ":".join([fileName, str(-patch._lineschanged[0])])
                    
                    # Try applying the subpatch as normal
                    subpatch_run_success = patch.Apply(fileName)
                    if subpatch_run_success:
                        successful_subpatches.append(subpatch_name)
                    else:
                        # Compute the diff between patch and file
                        diff_obj = tm.find_diffs(patch, fileName)

                        if diff_obj.match_status == tm.Diff.MatchStatus.MATCH_FOUND:
                            added_line_count = 0
                            removed_line_count = 0
                            patch_lines = patch.getLines()

                            for line in patch_lines:
                                if line[0] == parse.natureOfChange.ADDED:
                                    added_line_count += 1
                                elif line[0] == parse.natureOfChange.REMOVED:
                                    removed_line_count += 1

                            applied_percentage = 100 - (len(diff_obj.added_diffs) + len(diff_obj.removed_diffs))/(added_line_count+removed_line_count)*100

                            # Exact Patch Has Already Been Applied
                            if len(diff_obj.context_diffs) == 0 and len(diff_obj.added_diffs) == 0 and len(diff_obj.removed_diffs) == 0 and len(diff_obj.additional_lines) == 0:
                                successful_subpatches.append(subpatch_name)

                            # No lines between the context lines other than parts of the patch (currently only case where we can apply patches)
                            elif len(diff_obj.additional_lines) == 0: 
                                # We should not apply the patch, context changes affect the code
                                if are_context_changes_important(diff_obj):
                                    failed_subpatches_with_matched_code.append((applied_percentage, subpatch_name, diff_obj.match_start_line))
                                    
                                # We try to apply the patch, context changes are not important
                                # The case below is only for cases where the context is the only thing that is changed or a line has been completely added or removed with no similar lines
                                else:
                                    new_patch_lines = [patch_lines[0]]
                                    context_diff_index = 0
                                    added_diff_index = 0
                                    removed_diff_index = 0
                                    set_new_patch_lines = True
                                    for line in patch_lines[1:]:
                                        if line[0] == parse.natureOfChange.CONTEXT:
                                            if context_diff_index < len(diff_obj.context_diffs) and diff_obj.context_diffs[context_diff_index].patch_line.strip() == line[1].strip():
                                                if diff_obj.context_diffs[context_diff_index].is_missing:
                                                    context_diff_index += 1
                                                    continue
                                                new_context_line = diff_obj.context_diffs[context_diff_index].file_line
                                                new_patch_lines.append((parse.natureOfChange.CONTEXT, new_context_line))
                                                context_diff_index += 1
                                            else:
                                                new_patch_lines.append(line)
                                        elif line[0] == parse.natureOfChange.ADDED:
                                            if added_diff_index < len(diff_obj.added_diffs) and diff_obj.added_diffs[added_diff_index].patch_line.strip() == line[1].strip():
                                                new_patch_lines.append(line)
                                                added_diff_index += 1
                                            else:
                                                new_patch_lines.append((parse.natureOfChange.CONTEXT, line[1]))
                                        elif line[0] == parse.natureOfChange.REMOVED:
                                            if removed_diff_index < len(diff_obj.removed_diffs) and diff_obj.removed_diffs[removed_diff_index].patch_line.strip() == line[1].strip():
                                                new_patch_lines.append(line)
                                                removed_diff_index += 1
                                            # need to check case where similar line is added

                                    if set_new_patch_lines:
                                        old_patch_lines = patch._lines
                                        patch._lines = new_patch_lines
                                        if patch.Apply(fileName):
                                            successful_subpatches.append(subpatch_name)
                                        else:
                                            # TODO: Sometimes, moving lines causes an issue, will have to think of a fix that doesn't break a ton of cases
                                            print("Issue with current assumption in terms of what patches can be applied")
                                            print(patch)
                                            failed_subpatches_with_matched_code.append((applied_percentage, subpatch_name, diff_obj.match_start_line))
                                    else:
                                        failed_subpatches_with_matched_code.append((applied_percentage, subpatch_name, diff_obj.match_start_line))

                            else:
                                failed_subpatches_with_matched_code.append((applied_percentage, subpatch_name, diff_obj.match_start_line))

                        else:
                            subpatches_without_matched_code.append(subpatch_name)

            if len(successful_subpatches) > 0:
                print("\nHere are the subpatches that applied successfully:")
                print("\n".join(successful_subpatches))
            
            if len(failed_subpatches_with_matched_code) > 0:
                failed_subpatches_with_matched_code.sort()
                print("\nHere are the subpatches that did not apply automatically, but we think we found where the patch should be applied")
                print("Note that if a subpatch has an Applied Percentage of 100%, that means that the context may have changed in ways that affect the code")
                for applied_percentage, sp_name, line_number in failed_subpatches_with_matched_code:
                    print("{} - Line Number: {} - Applied Percentage: {}%".format(sp_name, line_number, applied_percentage))

            if len(subpatches_without_matched_code) > 0:
                print("\nHere are the subpatches that did not apply, and we could not find where the patch should be applied")
                print("\n".join(subpatches_without_matched_code))

        return 1


def main():
    if (args.reverse):
        apply_reverse(args.pathToPatch)
    else:
        apply(args.pathToPatch)

if __name__ == "__main__":
    args = get_args()
    main()
