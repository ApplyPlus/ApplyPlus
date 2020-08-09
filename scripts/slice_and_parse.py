import os, subprocess
import tempfile as tfile
import re
from enum import Enum

class SliceFields(Enum):
    FILEPATH = 0
    FUNCTION_NAME = 1
    VARIABLE_NAME = 2
    DEF = 3
    USE = 4
    DVARS = 5
    POINTERS = 6
    CFUNCS = 7

class SliceParser:
    def __init__(self, file):
        self.file = file

    def slice_parse(self):
        p = subprocess.Popen(["srcml", f"{self.file}", "--position"], stdout=subprocess.PIPE)
        out, err = p.communicate()

        fd, path = tfile.mkstemp(suffix=".xml", prefix="temp")
        try:
            with os.fdopen(fd, "w") as tmpo:
                tmpo.write(str(out, "utf-8"))
            p = subprocess.Popen(
               ["build/bin/srcSlice", f"{path}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out, err = p.communicate()

            str_out = out.decode("utf-8")
            slice_dict = {}

            for line in str_out.splitlines():
                
                # TODO: observe issue that arrises for patch CVE-2014-9710
                
                file_data = re.split(",\s*(?![^{}]*\})", line)
                if len(file_data) == 8:

                    slice_dict[file_data[1]] = {}
                
                    slice_dict[file_data[1]][file_data[2]] = []
                    
                    slice_dict[file_data[1]][file_data[2]].append(file_data[0])
                    slice_dict[file_data[1]][file_data[2]].append(file_data[1])
                    slice_dict[file_data[1]][file_data[2]].append(file_data[2])
                    
                    slice_dict[file_data[1]][file_data[2]].append((
                        file_data[3].split("{", 1)[1].split("}")[0]
                    ))
                    slice_dict[file_data[1]][file_data[2]].append((
                        file_data[4].split("{", 1)[1].split("}")[0]
                    ))
                    slice_dict[file_data[1]][file_data[2]].append((
                        file_data[5].split("{", 1)[1].split("}")[0]
                    ))
                    slice_dict[file_data[1]][file_data[2]].append((
                        file_data[6].split("{", 1)[1].split("}")[0]
                    ))
                    slice_dict[file_data[1]][file_data[2]].append((
                        file_data[7].split("{", 1)[1].rsplit("}", 1)[0]
                    ))

            return slice_dict

        finally:
            os.remove(path)


# testing
# file = "../../../msm-3.10/fs/file_table.c"
# sp = SliceParser(file)
# slice_dict = sp.slice_parse()
# function_slice = slice_dict["files_init"]
# assert(function_slice['mempages'][SliceFields.FUNCTION_NAME.value], 'files_init')

