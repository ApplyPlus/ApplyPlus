import os
import patchParser as parse

def checkFileExistsElsewhere(patch):
    """
    A small percentage of patches fail because the file has changed locations within the repo.
    If the file were in its original location, the patch would have applied without issues.
    
    To try to avoid this error, this method goes through all the directories
    from current dirrectory and checks to see if this file exists.

    If it does, it warns the user that the file has moved.
    NOTE: This method assumes the patch has failed and we are looking for solutions

    TODO: Attempt to apply the patch once a user has selected a file
    """

    toFind = patch.getFileName().split('/')[-1]
    currentdir = os.getcwd()
    matched_file_locations = []
    for subdir, dirs, files in os.walk(currentdir):
        for file in files:
            if (file == toFind):
                matched_file_locations.append(os.path.join(subdir, file))
    
    if len(matched_file_locations) == 0:
        print("A file with the filename could not be found in the current directory. Maybe the file has been deleted.")
    else:
        print("Here are the locations of files with the same filename as the missing file:")
        for i in range(len(matched_file_locations)):
            print("{} : {}".format(i, matched_file_locations[i]))
        
        to_apply_file_index = input("Select the file you would like to apply the patch to by entering the number next to it. Enter anything else to do nothing\n")

        try:
            to_apply_file_index = int(to_apply_file_index)
            if 0 <= to_apply_file_index and to_apply_file_index < len(matched_file_locations):
                # TODO: Update this once we have methods to attempt to apply a subpatch
                pass
        except ValueError:
            pass

# Testing
# patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2014-8172.patch")
# patch_file.getPatch()
# checkFileExistsElsewhere(patch_file.patches[0])