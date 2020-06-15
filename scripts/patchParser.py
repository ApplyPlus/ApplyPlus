<<<<<<< HEAD
class Patch():
    
    def __init__(self, patchname):
=======
from enum import Enum


class natureOfChange(Enum):
    ADDED = 1
    REMOVED = -1
    CONTEXT = 0


class Patch():
    
    def __init__(self, filename):
>>>>>>> f364adaa7fba11c7532c30fbd339c9b460e14d8f
        """
        Constructor
        --------------------------
        Gets patch name as input
        --------------------------
        _lines is a list of tuples of the format-
        [(<nature_of_change>, <change>),(<nature_of_change>, <change>),...,]
<<<<<<< HEAD
        Nature of Change can be one of = {Added, Removed, Rontext}
        """
        self._patchname = patchname
=======
        Nature of Change can be one of the enums defined in natureOfChange (ADDED, REMOVED, CONTEXT)
        """
        self._fileName = filename
>>>>>>> f364adaa7fba11c7532c30fbd339c9b460e14d8f
        self._lines = []
    
    def __str__(self):
        """
        Overloaded print function
        """
<<<<<<< HEAD
        toReturn = "filename: {} \n".format(self._patchname)
        for line in self._lines:
            if line[0] == "added":
                toReturn += "Type: {}   ||{}\n".format(line[0], line[1])
            else:
                toReturn += "Type: {} ||{}\n".format(line[0], line[1])
        return toReturn

    def addLines(self, lineToAdd, lineType):
=======
        toReturn = "filename: {} \n".format(self._fileName)
        for line in self._lines:
            if line[0] == natureOfChange.ADDED:
                toReturn += "Type: {}   ||{}\n".format(line[0].name, line[1])
            else:
                toReturn += "Type: {} ||{}\n".format(line[0].name, line[1])
        return toReturn

    def addLines(self, lineType, lineToAdd):
>>>>>>> f364adaa7fba11c7532c30fbd339c9b460e14d8f
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
<<<<<<< HEAD
        Nature of Change can be one of = {Added, Removed, Rontext}
=======
        Nature of Change can be one of the enums defined in natureOfChange (ADDED, REMOVED, CONTEXT)
>>>>>>> f364adaa7fba11c7532c30fbd339c9b460e14d8f
        """
        return self._lines
    
    def getFileName(self):
        """ 
        Accessor to get file name
        """
<<<<<<< HEAD
        return self._patchname
=======
        return self._fileName
>>>>>>> f364adaa7fba11c7532c30fbd339c9b460e14d8f


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

    def runPatch(self):
        """ 
        Returns an empty string if patch successfully runs 
        else returns the exact error message as a string
        """
        pass

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

                if patchObj.getFileName() != 'temp' :  # To avoid pushing an empty list in 1st iteration
                    self.patches.append(patchObj)
                filename = line[11:].split()[0][1:]
                patchObj = Patch(filename)

            elif line[0:2] == '@@':
                contextline=line[2:].split(' @@ ')[-1]

                if len(patchObj.getLines()) != 0:
                    filename = patchObj.getFileName()
                    self.patches.append(patchObj)
                    patchObj = Patch(filename)
    
<<<<<<< HEAD
                patchObj.addLines(contextline, 'Context')
            
            elif line[0]=="-" and line[0:3] != "---":
                contextline = line[1:]
                patchObj.addLines(contextline, 'Removed')
            
            elif line[0] == "+" and line[0:3] != "+++":
                contextline = line[1:]
                patchObj.addLines(contextline, 'Added')

            else:
                patchObj.addLines(line, 'Context')

        self.patches.append(patchObj)

=======
                patchObj.addLines(natureOfChange.CONTEXT, contextline, )
            
            elif line[0]=="-":
                contextline = line[1:]
                patchObj.addLines(natureOfChange.REMOVED, contextline)
            
            elif line[0] == "+":
                contextline = line[1:]
                patchObj.addLines(natureOfChange.ADDED, contextline)

            else:
                patchObj.addLines(natureOfChange.CONTEXT, line)

        self.patches.append(patchObj)
>>>>>>> f364adaa7fba11c7532c30fbd339c9b460e14d8f
