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
    To do: Ask user if we should apply to the moved file
    """
    
    toFind = patch.getFileName().split('/')[-1]
    currentdir = os.getcwd()
    for subdir, dirs, files in os.walk(currentdir):
        for file in files:
            print(os.path.join(file))
            if (file == toFind):
                print("File with the same as {} name found: at {}".format(toFind,
                    os.path.join(subdir, file)))
                print("Maybe the file the patch is referring to has been moved?")

