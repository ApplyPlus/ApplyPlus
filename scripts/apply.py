import patchParser as parse
import check_file_exists_elsewhere as fileCheck

def main():
    print("Main called")
    patch_file = parse.PatchFile("patch.patch")
    patch_file.getPatch()
    fileCheck.checkFileExistsElsewhere(patch_file.patches[0])

if __name__ == "__main__":
    main()
