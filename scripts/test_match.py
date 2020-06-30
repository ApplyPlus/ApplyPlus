import diff_match_patch as dmp_module
import patchParser as parse 

dmp = dmp_module.diff_match_patch()
dmp.Match_Distance = 2000
# Match will not always start right at the beginning of the patch
PATCH_LENGTH_BUFFER = 50 

class Retry():
    def __init__(self, retry_times, retry_interval):
        self.retry_times = retry_times
        self.retry_interval = retry_interval

# Returns line number of match location, returns -1 if no match
def fuzzy_search(search_lines, file_name, patch_line_number, retry_obj=None):
    # TODO: Don't skip first line once the patch lines do not contain the line number of patch
    search_pattern = '\n'.join(search_lines[1:]) 

    file_lines = []
    cur_char = 0
    search_location = -1
    cur_line = 1
    line_to_char_dict = {}
    
    with open(file_name) as f:
        for line in f:
            line_to_char_dict[cur_line] = cur_char 
            cur_line += 1
            cur_char += len(line)
            file_lines.append(line)

        if patch_line_number in line_to_char_dict:
            search_location = line_to_char_dict[patch_line_number]
        # The case that the line number in the patch file is no longer valid, let's just search from middle for now
        else:
            search_location = cur_char//2

    file_str = "".join(file_lines)

    char_match_loc = dmp.match_main(file_str, search_pattern, search_location)

    if char_match_loc == -1 and retry_obj:
        for i in range(1, retry_obj.retry_times+1):
            search_above_line = patch_line_number + i * retry_obj.retry_interval
            search_below_line = patch_line_number - i * retry_obj.retry_interval

            if search_above_line in line_to_char_dict:
                search_above_res = dmp.match_main(file_str, search_pattern, line_to_char_dict[search_above_line])
                if search_above_res != -1:
                   char_match_loc = search_above_res
                   break 
            if search_below_line in line_to_char_dict:
                search_below_res = dmp.match_main(file_str, search_pattern, line_to_char_dict[search_below_line])
                if search_below_res != -1:
                   char_match_loc = search_below_res
                   break 

    if char_match_loc != -1:
        return file_str[:char_match_loc].count("\n") + 1
    else:
        return -1

def search_for_already_applied(patch_lines, file_name, retry_obj=None):
    search_lines = []
    for line in patch_lines:
        if line[0] != parse.natureOfChange.REMOVED:
            search_lines.append(line[1])
    
    # TODO: Change this to automatically grab line number
    patch_line_number = 1937 
    return fuzzy_search(search_lines, file_name, patch_line_number, retry_obj)

def is_already_applied(patch_lines, file_name, retry_obj=None):
    match_start_line = search_for_already_applied(patch_lines, file_name, retry_obj)
    if match_start_line == -1:
        return False

    with open(file_name) as f:
        file_lines = f.readlines()[match_start_line:]

    deleted_lines = set() 
    added_lines = set()
    for line in file_lines:
        if line[0] == parse.natureOfChange.REMOVED:
            deleted_lines.add(line[1])
        elif line[0] == parse.natureOfChange.ADDED:
            added_lines.set(line[1])
        
    deleted_lines_not_applied = set()
    for i in range(len(patch_lines) + PATCH_LENGTH_BUFFER):
        if i >= len(file_lines):
            break
        if file_lines[i] in deleted_lines:
            deleted_lines_not_applied.add(file_lines[i])
        if file_lines[i] in added_lines:
            del added_lines[file_lines[i]]

    # Can also modify this to return the lines not applied if needed    
    if len(deleted_lines_not_applied) == 0 and len(added_lines) == 0:
        return True
    
# Testing
# patch_file = parse.PatchFile("../patches/CVE-2014-5206.patch")
# patch_file.getPatch()
# print(is_already_applied(patch_file.patches[0]._lines, "../../msm-3.10/fs/namespace.c", Retry(2,100)))