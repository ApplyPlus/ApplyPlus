import patchParser as parse
import test_match as match
import slice_and_parse as slice
import diff_match_patch as dmp_module

# Tested Patch Files
# patch_file_name = "../patches/CVE-2016-6828.patch"
# patch_file_name = "../patches/CVE-2016-4482.patch"
# patch_file_name = "../patches/CVE-2015-8964.patch"
# patch_file_name = "../patches/CVE-2016-2550.patch"
# patch_file_name = "../patches/CVE-2016-3672.patch"
# patch_file_name = "../patches/CVE-2016-4565.patch"
# patch_file_name = "../patches/CVE-2014-8172.patch"
# patch_file_name = "../patches/CVE-2013-7281.patch"
# patch_file_name = "../patches/CVE-2013-7348.patch"
# patch_file_name = "../patches/CVE-2014-7822.patch"
# patch_file_name = "../patches/CVE-2014-8172.patch"
# patch_file_name = "../patches/CVE-2014-8481.patch"
# patch_file_name = "../patches/CVE-2014-9090.patch"
# patch_file_name = "../patches/CVE-2014-9322.patch"
# patch_file_name = "../patches/CVE-2014-9644.patch"
# patch_file_name = "../patches/CVE-2014-9710.patch"
# patch_file_name = "../patches/CVE-2015-0274.patch"
# patch_file_name = "../patches/CVE-2015-0275.patch"
# patch_file_name = "../patches/CVE-2015-1333.patch"
# patch_file_name = "../patches/CVE-2015-1805.patch"
# patch_file_name = "../patches/CVE-2015-2672.patch"
# patch_file_name = "../patches/CVE-2015-2925.patch"
# patch_file_name = "../patches/CVE-2015-3212.patch"
# patch_file_name = "../patches/CVE-2015-4001.patch"
# patch_file_name = "../patches/CVE-2015-4176.patch"
# patch_file_name = "../patches/CVE-2015-4692.patch"
# patch_file_name = "../patches/CVE-2015-4700.patch"
# patch_file_name = "../patches/CVE-2015-5697.patch"
# patch_file_name = "../patches/CVE-2015-6937.patch"
# patch_file_name = "../patches/CVE-2015-7513.patch"
# patch_file_name = "../patches/CVE-2015-7613.patch"
# patch_file_name = "../patches/CVE-2015-7990.patch"
# patch_file_name = "../patches/CVE-2015-8104.patch"
# patch_file_name = "../patches/CVE-2015-8215.patch"
# patch_file_name = "../patches/CVE-2015-8543.patch"
# patch_file_name = "../patches/CVE-2015-8575.patch"
# patch_file_name = "../patches/CVE-2015-8816.patch"
# patch_file_name = "../patches/CVE-2015-8845.patch"
# patch_file_name = "../patches/CVE-2016-0774.patch"
# patch_file_name = "../patches/CVE-2016-0823.patch"
# patch_file_name = "../patches/CVE-2016-1237.patch"
# patch_file_name = "../patches/CVE-2016-2061.patch"
# patch_file_name = "../patches/CVE-2016-2069.patch"
# patch_file_name = "../patches/CVE-2016-2143.patch"
# patch_file_name = "../patches/CVE-2016-2441.patch"
# patch_file_name = "../patches/CVE-2016-2442.patch"
# patch_file_name = "../patches/CVE-2016-2465.patch"
# patch_file_name = "../patches/CVE-2016-2489.patch"
# patch_file_name = "../patches/CVE-2016-2550.patch"
# patch_file_name = "../patches/CVE-2016-3139.patch"
# patch_file_name = "../patches/CVE-2016-3672.patch"
# patch_file_name = "../patches/CVE-2016-4482.patch"
# patch_file_name = "../patches/CVE-2016-4482.patch"
# patch_file_name = "../patches/CVE-2016-4565.patch"
# patch_file_name = "../patches/CVE-2016-7117.patch"
# patch_file_name = "../patches/CVE-2016-7042.patch"
# patch_file_name = "../patches/CVE-2016-6787.patch"
# patch_file_name = "../patches/CVE-2016-6327.patch"
# patch_file_name = "../patches/CVE-2016-4470.patch"
# patch_file_name = "../patches/CVE-2016-4440.patch"
# patch_file_name = "../patches/CVE-2016-3070.patch"
# patch_file_name = "../patches/CVE-2015-8966.patch"
# patch_file_name = "../patches/CVE-2015-8964.patch"
# patch_file_name = "../patches/CVE-2015-8963.patch"
# patch_file_name = "../patches/CVE-2015-8962.patch"
# patch_file_name = "../patches/CVE-2015-8961.patch"
# patch_file_name = "../patches/CVE-2015-8952.patch"

# GOLDEN
# patch_file_name = "../patches/CVE-2015-0572.patch"

# DEFINE STATEMENTS ...
# patch_file_name = "../patches/CVE-2014-9803.patch"


def context_changes(patch_file_name):
    patch_file = parse.PatchFile(patch_file_name)
    patch_file.getPatch()

    file_name = patch_file.patches[0].getFileName()
    file_name = f"../../../msm-3.10{file_name}"

    sp = slice.SliceParser(file_name)
    file_slice = sp.slice_parse()

    diff_obj = match.find_diffs(
        patch_file.patches[0],
        file_name,
        try_already_applied=True,
        retry_obj=match.Retry(2, 100),
    )

    if diff_obj.match_status == match.Diff.MatchStatus.MATCH_FOUND:
        if diff_obj.context_diffs:
            for context_diffs in diff_obj.context_diffs:
                if context_diffs.match_ratio > match.LEVENSHTEIN_RATIO:
                    function_name = context_diffs.function_for_patch
                    if function_name:
                        function_name = function_name.split("(")[0].split()[-1]

                        if "(" in context_diffs.file_line and ")" in context_diffs.file_line:
                            # handle function context diff
                            print(
                                f"We noticed a context-related difference between the function in the source code [{context_diffs.file_line}]"
                            )
                            print(
                                f"We are suggesting to replace this function with [{context_diffs.patch_line}]"
                            )
                            break

                        diff_match = dmp_module.diff_match_patch()
                        line_patch_diffs = diff_match.diff_main(
                            context_diffs.file_line, context_diffs.patch_line
                        )

                        print(line_patch_diffs)
                        # handles R-Value Variables
                        for diff in line_patch_diffs:
                            if diff[0] == 0 and diff[1].rstrip().endswith("="):
                                print(
                                    "[SLICER_MESSAGE]: An R-Value has been changed, the slicer does not have information about R-Value variables."
                                )
                                break

                        # handle l-value variable context conflict
                        for diff in line_patch_diffs:
                            if diff[0] == 0 and diff[1].rstrip().startswith("="):
                                # retrive L-Value variable being changed
                                file_var = [
                                    item for item in line_patch_diffs if item[0] == -1
                                ][0]

                                var_statistics = file_slice[function_name][file_var]
                                print(var_statistics)
                    else:
                        print("WARNING: Function was not supplied. Skipping this patch.")

                else:
                    print("The match ratio between the source and patch code was low")
                    print(
                        f"We received a match ratio of {context_diffs.match_ratio}, expected a ratio greater than {match.LEVENSHTEIN_RATIO}"
                    )
        else:
            print("[SLICER_WARNING]: No context related issues found")
    else:
        print("[SLICER_WARNING]: A context match was not found.")
