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

# TODO: Update this to actually run subpatch once code for that has been merged
def run_subpatch(patch):
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
        try_subpatches = input("Would you like to try and apply subpatches? [Y/n]\n")
        if try_subpatches.upper() == "Y":
            successful_subpatches = []
            unsuccessful_subpatches = []
            for patch in patch_file.patches:
                # [1:] is used to remove the leading slash
                if patch._fileName[1:] in does_not_apply:
                    subpatch_run_success = run_subpatch(patch) 
                    if subpatch_run_success:
                        successful_subpatches.append(patch)
                    else:
                        unsuccessful_subpatches.append(patch)
            
            if len(successful_subpatches) != 0:
                print("Here are the subpatches that applied successfully:")
                for patch in successful_subpatches:
                    print(":".join([patch._fileName, str(-patch._lineschanged[0])]))
            
            subpatches_with_matched_code = []
            subpatches_without_matched_code = []

            for patch in unsuccessful_subpatches:
                subpatch_name =  ":".join([patch._fileName, str(-patch._lineschanged[0])])
                patch_lines = patch._lines
                line_number = patch._lineschanged[2]

                file_path = os.path.join(os.getcwd(), patch._fileName[1:])

                # Try searching for patch not applied in file
                search_lines = [line[1] for line in tm.get_file_without_patch(patch_lines)]
                match_start_line = tm.fuzzy_search(search_lines, file_path, line_number)

                # Try searching for patch applied in file
                if match_start_line == -1:
                    search_lines = [line[1] for line in tm.get_file_with_patch(patch_lines)]
                    match_start_line = tm.fuzzy_search(search_lines, file_path, line_number)
                
                if match_start_line == -1:
                    subpatches_without_matched_code.append(subpatch_name)
                else:
                    subpatches_with_matched_code.append((subpatch_name, match_start_line))

            print("Here are the subpatches that did not apply, but we think we found where the patch should be applied")
            for sp_name, line_number in subpatches_with_matched_code:
                print("{} - Line Number: {}".format(sp_name, line_number))

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
