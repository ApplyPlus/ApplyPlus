import argparse

import patchParser as parse
import check_file_exists_elsewhere as fileCheck


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reverse", help="Apply a patch in reverse files and/or to the index")

    args = parser.parse_args()
    return args


def main():
    patch_file = parse.PatchFile("patch.patch")
    patch_file.getPatch()
    fileCheck.checkFileExistsElsewhere(patch_file.patches[0])

if __name__ == "__main__":
    args = get_args()
    print(args.apply)
    main()
