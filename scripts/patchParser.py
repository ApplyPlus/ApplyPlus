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

    def _to_raw(self, string):
        """ Private helper method to return raw string"""
        return fr"{string}"
    def canApply(self, applyTo):
        """
        Returns True if this patch can be applied, false otherwise
        """
        orgPatch = open(applyTo).readlines()
        orgPatch = [s.strip("\n").encode(
            'ascii', "ignore").decode('unicode_escape', "ignore") for s in orgPatch]
        for checkLines in range(len(orgPatch)):
            # Check if first line of patch exists
            if (orgPatch[checkLines].strip() == self._to_raw(self._lines[1][1]).strip()):
                patch_found_flag = True
                blank_line_offset_file = 0
                added_offset = 0
                ite = 2
                while ite < len(self._lines):
                    original_patch_offset = checkLines + ite-1-blank_line_offset_file - added_offset
                    if original_patch_offset >= len(orgPatch):
                        patch_found_flag = False
                        break
                    if self._lines[ite][0] == natureOfChange.ADDED and orgPatch[original_patch_offset].strip():
                        if orgPatch[original_patch_offset].strip() == self._lines[ite][1].strip():
                            pass
                            # self._lines[ite] = (natureOfChange.CONTEXT, self._lines[ite][1])
                        else:
                            added_offset += 1
                    elif (orgPatch[original_patch_offset].strip() != self._lines[ite][1].strip()):
                        if len(orgPatch[original_patch_offset].strip()) == 0:
                            blank_line_offset_file -= 1
                            ite -= 1
                        elif len(self._lines[ite][1].strip()) == 0:
                            blank_line_offset_file += 1
                        else:
                            patch_found_flag = False
                            break
                    ite += 1
                if patch_found_flag:
                    return True
        return False

    def Apply(self, applyTo):
        """
        If patch can be applied, this method
        applies it. 
        """
        if self.canApply(applyTo):
            orgPatch = open(applyTo).readlines()
            orgPatch = [s.strip("\n").encode(
                'ascii', "ignore").decode('unicode_escape', "ignore") for s in orgPatch]
            for checkLines in range(len(orgPatch)):
                # Check if first line of patch exists
                if (orgPatch[checkLines].strip() == self._to_raw(self._lines[1][1]).strip()):
                    patch_found_flag = True
                    blank_line_offset_file = 0
                    added_offset = 0
                    ite = 2
                    while ite < len(self._lines):
                        original_patch_offset = checkLines + ite-1-blank_line_offset_file - added_offset
                        if original_patch_offset >= len(orgPatch):
                            patch_found_flag = False
                            break
                        if self._lines[ite][0] == natureOfChange.ADDED and orgPatch[original_patch_offset].strip():
                            if orgPatch[original_patch_offset].strip() == self._lines[ite][1].strip():
                                self._lines[ite] = (natureOfChange.CONTEXT, self._lines[ite][1])
                            else:
                                added_offset += 1
                        elif (orgPatch[original_patch_offset].strip() != self._lines[ite][1].strip()):
                            if len(orgPatch[original_patch_offset].strip()) == 0:
                                blank_line_offset_file -= 1
                                ite -= 1
                            elif len(self._lines[ite][1].strip()) == 0:
                                blank_line_offset_file += 1
                            else:
                                patch_found_flag = False
                                break
                        ite += 1
                    if patch_found_flag:
                        #If the next line runs, we know the patch is applied here
                        ite2 = 0
                        ite3 = 1
                        goal = len(self._lines)
                        while(ite2 < goal and ite3 < len(self._lines)):

                            if(self._lines[ite3][0] == natureOfChange.REMOVED):
                                goal -= 1
                                orgPatch.pop(checkLines+ite2)
                                ite3 += 1
                            elif(self._lines[ite3][0] == natureOfChange.ADDED):
                                orgPatch.insert(
                                    checkLines+ite2, self._lines[ite3][1])
                                ite2 += 1
                                ite3 += 1
                            elif(self._lines[ite3][0] == natureOfChange.CONTEXT):
                                if (self._lines[ite3][1].strip() != orgPatch[checkLines+ite2].strip()):
                                    if (len(self._lines[ite3][1].strip()) == 0):
                                        ite3 += 1
                                    else:
                                        ite2 += 1
                                else:
                                    ite2 += 1
                                    ite3 += 1
                        writeobj = open(applyTo, "w")
                        for i in orgPatch:
                            i= i.replace('\n', '\\n')
                            writeobj.write(i+"\n")
                        writeobj.close()
                        return True

        return False
            
        

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
                contextline = line[2:].split(' @@ ')[-1]
                if len(patchObj.getLines()) != 0:
                    filename = patchObj.getFileName()
                    self.patches.append(patchObj)
                    patchObj = Patch(filename)
                    patchObj.setLinesChanged(line)
                else:
                    patchObj.setLinesChanged(line)

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


