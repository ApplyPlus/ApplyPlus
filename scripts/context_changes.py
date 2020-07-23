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

diff_obj = match.find_diffs(
    patch_file.patches[0],
    source_file,
    try_already_applied=True,
    retry_obj=match.Retry(2, 100),
)

if diff_obj.match_status == match.Diff.MatchStatus.MATCH_FOUND:
    first_diff_context = diff_obj.context_diffs[0]

    if first_diff_context.match_ratio >= match.LEVENSHTEIN_RATIO:
        file_line = first_diff_context.file_line
        # TODO: figure out what this is
        is_missing = first_diff_context.is_missing
        patch_line = first_diff_context.patch_line

        fl_function_name = file_line.split("(")[0].split()[-1]
        patch_file_name = patch_line.split("(")[0].split()[-1]
        if fl_function_name:
            # handle function context diff
            print(
                f"We noticed a context-related difference between the function in the source code {fl_function_name}"
            )
            print(f"We are suggesting to replace this function with {patch_file_name}")
            print("Would you like to proceed with this change?")


# if only the match is found we will run our code
# if diff_obj.match_status == match.Diff.MatchStatus.MATCH_FOUND.value:
#    for context_diff in diff.diff_obj.context_diffs:
#        if context_diff.match_ratio >= match.LEVENSHTEIN_RATIO:


for x in diff_obj.context_diffs:
    print(x.language_specific_diff.diff_tokens)
    print(x.language_specific_diff)  # .diff_tokens)
    print(x.match_ratio)
    print(x.file_line)
    print(x.is_missing)
    print(x.patch_line)


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

