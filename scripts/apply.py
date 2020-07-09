import argparse

import patchParser as parse
import check_file_exists_elsewhere as fileCheck


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



def apply(pathToPatch):
    print("apply called")
    patch_file = parse.PatchFile(pathToPatch)
    patch_file.runPatch()
    if(patch_file.runSuccess == True):
        print("Successfully applied")
        return 0
    else:
        print("Patch failed with error:")
        print(patch_file.runResult)
        return 1


def main():
    if (args.reverse):
        apply_reverse(args.pathToPatch)
    else:
        apply(args.pathToPatch)

if __name__ == "__main__":
    args = get_args()
    main()
