import os, subprocess, sys
import tempfile as tfile
import re
from enum import Enum


class SliceParser:
    def __init__(self, file):
        self.file = file

    def slice_parse(self):
        p = subprocess.Popen(
            ["srcml", f"{self.file}", "--position"], stdout=subprocess.PIPE
        )
        out, err = p.communicate()

        if err:
            return None

        fd, path = tfile.mkstemp(suffix=".xml", prefix="temp")
        try:
            with os.fdopen(fd, "w") as tmpo:
                tmpo.write(str(out, "utf-8"))

            if sys.platform.startswith("darwin"):
                src_slice_path = "../vulnerableforks/scripts/patch_context/srcSliceBuilds/macOS/srcslice-mac"
            else:
                src_slice_path = "../vulnerableforks/scripts/patch_context/srcSliceBuilds/ubuntu/srcslice-ubuntu"

            p = subprocess.Popen(
                [
                    src_slice_path,
                    f"{path}",
                ],
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

                    slice_dict[file_data[1]][file_data[2]].append(
                        (file_data[3].split("{", 1)[1].split("}")[0])
                    )
                    slice_dict[file_data[1]][file_data[2]].append(
                        (file_data[4].split("{", 1)[1].split("}")[0])
                    )
                    slice_dict[file_data[1]][file_data[2]].append(
                        (file_data[5].split("{", 1)[1].split("}")[0])
                    )
                    slice_dict[file_data[1]][file_data[2]].append(
                        (file_data[6].split("{", 1)[1].split("}")[0])
                    )
                    slice_dict[file_data[1]][file_data[2]].append(
                        (file_data[7].split("{", 1)[1].rsplit("}", 1)[0])
                    )

            return slice_dict

        finally:
            os.remove(path)
