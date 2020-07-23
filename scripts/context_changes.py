import patchParser as parse
import test_match as match
import slice_and_parse as slice

patch_file_name = "../patches/CVE-2016-6828.patch"
patch_file = parse.PatchFile(patch_file_name)
patch_file.getPatch()

source_file = patch_file.patches[0].getFileName()
source_file = f"../../../msm-3.10{source_file}"

sp = slice.SliceParser(source_file)
sliced_file = sp.slice_parse()

function_name = patch_file.patches[0].getLines()[0][1]
function_name = function_name.split("(")[0].split()[-1]

# diff_obj = match.find_diffs(patch_file.patches[0], "/Users/yuvika/Desktop/UW_Research/msm-3.10/include/net/tcp.h", try_already_applied=True, retry_obj=match.Retry(2,100))
# print(diff_obj.match_status)
# print(diff_obj.context_diffs)
# print(diff_obj.additional_lines)
# for x in diff_obj.context_diffs:
# print(x.language_specific_diff) #.diff_tokens)
# print(x.match_ratio)
# print(x.file_line)
# print(x.is_missing)
# print(x.patch_line)

