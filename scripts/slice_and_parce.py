import os, subprocess
import tempfile as tfile
import re

file = "../../../msm-3.10/fs/file_table.c"

file_xml = subprocess.check_output(f"srcML {file}", shell=True)

p = subprocess.Popen(["srcML", f"{file}"], stdout=subprocess.PIPE)
out, err = p.communicate()

fd, path = tfile.mkstemp(suffix=".xml", prefix="temp")
try:
    with os.fdopen(fd, "w") as tmpo:
        # do stuff with temp file
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
        file_data = re.split(",\s*(?![^{}]*\})", line)
        dict_key = file_data[1] + "/" + file_data[2]

        slice_dict[dict_key] = {}
        slice_dict[dict_key]["FilePath"] = file_data[0]
        slice_dict[dict_key]["FunctionName"] = file_data[1]
        slice_dict[dict_key]["VariableName"] = file_data[2]
        slice_dict[dict_key]["DefLines"] = file_data[3].split("{", 1)[1].split("}")[0]
        slice_dict[dict_key]["UsesLines"] = file_data[4].split("{", 1)[1].split("}")[0]
        slice_dict[dict_key]["dvars"] = file_data[5].split("{", 1)[1].split("}")[0]
        slice_dict[dict_key]["pointers"] = file_data[6].split("{", 1)[1].split("}")[0]
        slice_dict[dict_key]["cfuncs"] = file_data[7].split("{", 1)[1].rsplit("}", 1)[0]

except Exception as e:
    print(e)
    print("s")
finally:
    os.remove(path)
