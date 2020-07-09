from enum import Enum
import re
import subprocess

class natureOfChange(Enum):
    ADDED = 1
    REMOVED = -1
    CONTEXT = 0


class Patch():

    def __init__(self, filename):
        """
        Constructor
        --------------------------
        Gets patch name as input
        --------------------------
        _lines is a list of tuples of the format-
        [(<nature_of_change>, <change>),(<nature_of_change>, <change>),...,]
        Nature of Change can be one of the enums defined in natureOfChange (ADDED, REMOVED, CONTEXT)
        _lineschanged stores the lines changed info for a patch. ie- The data found between @@s
        """
        self._fileName = filename
        self._lines = []
        self._lineschanged = [-1,-1,-1,-1]

    def __str__(self):
        """
        Overloaded print function
        """
        toReturn = "filename: {} \n".format(self._fileName)
        for line in self._lines:
            if line[0] == natureOfChange.ADDED:
                toReturn += "Type: {}   ||{}\n".format(line[0].name, line[1])
            else:
                toReturn += "Type: {} ||{}\n".format(line[0].name, line[1])
        return toReturn

    def addLines(self, lineType, lineToAdd):
        """ 
        Method used to add a line to a patch file
        """
        self._lines.append((lineType, lineToAdd))

    def getLines(self):
        """
        Accessor to get lines stored in patch
        --------------------------
        Returns a list of tuples of the format-
        [(<nature_of_change>, <change>),(<nature_of_change>, <change>),...,]
        Nature of Change can be one of the enums defined in natureOfChange (ADDED, REMOVED, CONTEXT)
        """
        return self._lines

    def getFileName(self):
        """ 
        Accessor to get file name
        """
        return self._fileName

    def setLinesChanged(self, rawData):
        """
        Method used to add lines changed info for a patch
        """
        pair = rawData.split("@@")[1].split(" ")[1:3]
        self._lineschanged[0] = int(pair[0].split(",")[0])
        self._lineschanged[1] = int(pair[0].split(",")[1])
        self._lineschanged[2] = int(pair[1].split(",")[0])
        self._lineschanged[3] = int(pair[1].split(",")[1])
        return

    def getLinesChanged(self):
        """ 
        Access the lines changed info for a patch
        return: A list of length 4.
        Eg: For @@ -20,7 +20,6 @@, 
        this method returns [-20, 7, 20, 6]
        """
        return self._lineschanged

    def canApply(self, applyTo):
        orgPatch = open(applyTo).readlines()
        for newline in self._lines:
            found = False;
            if (newline[1] != natureOfChange.ADDED):
                for sourceLine in orgPatch:
                    if(newline[1]==sourceLine):
                        found == True
                if found == False:
                    return False
        return True
    
    def Apply(self, applyTo):
        if (self.canApply(applyTo)):
            
        

class PatchFile():
    def __init__(self, pathToFile=""):
        """
        Constructor
        --------------------------
        Takes path to patch file as input
        --------------------------
        Patches is a list of objects of type patch
        """
        self.pathToFile = pathToFile
        self.patches = []
        self.runSuccess = False
        self.runResult = "Patch has not been run yet"

    def runPatch(self, reverse=False):
        """ 
        Returns an empty string if patch successfully runs 
        else returns the exact error message as a string

        If revert=True arg is provided, git apply --reverse is run.
        """
        if (reverse == True):
            result = subprocess.run(["git", "apply", "--reverse", self.pathToFile], capture_output=True)
        else:
            result = subprocess.run(
                ["git", "apply", self.pathToFile], capture_output=True)
        if result.returncode == 0:
            self.runSuccess = True
            self.runResult = "Patch ran successfully"
        else:
            self.runResult = result.stderr


            


    def getPatch(self):
        """
        A patch file has multiple patches.
        This method returns a list of patch objects
        each representing one patch  
        """

        fileObj = open(self.pathToFile)
        file = fileObj.read().rstrip()
        file = file.split('\n')

        patchObj = Patch("temp")

        for line in file:
            # print(line)
            # print("________________")

            if line[0:3] == "+++" or \
                    line[0:3] == "---" or \
                    line[0:5] == "index" or \
                    line == "\n":
                pass

            elif line[0:10] == "diff --git":

                if patchObj.getFileName() != 'temp':  # To avoid pushing an empty list in 1st iteration
                    self.patches.append(patchObj)
                filename = line[11:].split()[0][1:]
                patchObj = Patch(filename)

            elif line[0:2] == '@@':
                patchObj.setLinesChanged(line)
                if line[-2:] == "@@":
                    # To handle cases where the line number
                    #  is the only information available in that line
                    pass
                else:
                    contextline = line[2:].split(' @@ ')[-1]
                    if len(patchObj.getLines()) != 0:
                        filename = patchObj.getFileName()
                        self.patches.append(patchObj)
                        patchObj = Patch(filename)

                    patchObj.addLines(natureOfChange.CONTEXT, contextline, )

            elif line[0] == "-":
                contextline = line[1:]
                patchObj.addLines(natureOfChange.REMOVED, contextline)

            elif line[0] == "+":
                contextline = line[1:]
                patchObj.addLines(natureOfChange.ADDED, contextline)

            else:
                patchObj.addLines(natureOfChange.CONTEXT, line)

        self.patches.append(patchObj)


