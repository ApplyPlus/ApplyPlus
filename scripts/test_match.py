import diff_match_patch as dmp_module
import patchParser as parse 
from enum import Enum
import Levenshtein
from pycparser import c_lexer as clex

dmp = dmp_module.diff_match_patch()
dmp.Match_Distance = 2000
LEVENSHTEIN_RATIO = 0.8

"""
The purpose of this variable is because (start of matched code + patch length)
does not always contain the entire patch, so our matched code is the section from
(start of matched code) to (start of matched code + patch length + PATCH_LENGTH_BUFFER)
"""
PATCH_LENGTH_BUFFER = 10

# Defining the C Lexer
noop = lambda *args, **kwargs:None
def raise_lex_error(error_msg, _line, _col):
    error_msg_header = "Error occured while lexing file/patch - here is the error mesage:"
    fix_suggestion = "Either fix the lexing error, or stop scanning for C token diffs"
    raise Exception('\n'.join([error_msg_header, msg, fix_suggestion]))

lex = clex.CLexer(raise_lex_error, noop, noop, lambda x: True)
lex.build()

class Retry():
    def __init__(self, retry_times, retry_interval):
        self.retry_times = retry_times
        self.retry_interval = retry_interval

class Diff():
    class LineDiff():
        class TokenDiffType(Enum):
            PLAINTEXT = 0
            C = 1

        def __init__(self, patch_line, file_line="", is_missing=True, diff_tokens={}, match_ratio=-1):
            self.patch_line = patch_line
            self.file_line = file_line
            self.is_missing = is_missing
            self.diff_tokens = diff_tokens
            self.match_ratio = match_ratio

    class MatchStatus(Enum):
        NO_MATCH = 0
        MATCH_FOUND = 1

    def __init__(self, match_status, removed_diffs = [], added_diffs = [], context_diffs = [], additional_lines = []):
        self.match_status = match_status
        self.removed_diffs = removed_diffs
        self.added_diffs = added_diffs
        self.context_diffs = context_diffs
        self.additional_lines = additional_lines

"""
See docs for output format:
https://github.com/google/diff-match-patch/wiki/API
"""
def plaintext_token_diff(patch_line, file_line):
    diff_tokens = dmp.diff_main(patch_line, file_line)
    dmp.diff_cleanupSemantic(diff_tokens)
    return diff_tokens

"""
Returns a tuple (patch_tokens, file_tokens, diff_tokens) where:
- patch_tokens are tokens in the patch (in order)
- file_tokens are tokens in the file (in order)
- diff_tokens are tokens in the patch but not in the file (not ordered)
"""
def c_token_diff(patch_line, file_line):
    patch_tokens = []
    lex.input(patch_line)
    cur_token = lex.token()
    while cur_token: 
        patch_tokens.append((cur_token.type, cur_token.value))
        cur_token = lex.token()
       
    file_tokens = []
    lex.input(file_line)
    cur_token = lex.token()
    while cur_token:
        file_tokens.append((cur_token.type, cur_token.value))
        cur_token = lex.token()
    
    diff_tokens = list(set(patch_tokens) - set(file_tokens))

    return (patch_tokens, file_tokens, diff_tokens)

token_type_to_func = {
    Diff.LineDiff.TokenDiffType.PLAINTEXT : plaintext_token_diff,
    Diff.LineDiff.TokenDiffType.C : c_token_diff
}

# Returns line number of match location, returns -1 if no match
def fuzzy_search(search_lines, file_name, patch_line_number, retry_obj=None):
    search_pattern = '\n'.join(search_lines) 

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

def get_file_with_patch(patch_lines):
    search_lines = []
    for line in patch_lines:
        if line[0] != parse.natureOfChange.REMOVED:
            search_lines.append(line)
    
    # TODO: Remove this once context lines do not contain patch information
    search_lines = search_lines[1:]
    return search_lines

def get_file_without_patch_patch(patch_lines):
    search_lines = []
    for line in patch_lines:
        if line[0] != parse.natureOfChange.ADDED:
            search_lines.append(line)
    
    # TODO: Remove this once context lines do not contain patch information
    search_lines = search_lines[1:]
    return search_lines

# Returns an object containing information about the difference between a file and a patch
def find_diffs(patch_lines, file_name, try_already_applied = False, 
                retry_obj=None, token_diff_types = [Diff.LineDiff.TokenDiffType.PLAINTEXT]):
    # TODO: Get this automatically
    line_number = 36 
    
    if try_already_applied:
        search_lines_with_type = get_file_with_patch(patch_lines)
    else:
        search_lines_with_type = get_file_without_patch_patch(patch_lines)
    
    search_lines_without_type = [line[1] for line in search_lines_with_type]
    match_start_line = fuzzy_search(search_lines_without_type, file_name, line_number, retry_obj)

    if match_start_line == -1:
        return Diff(PatchVsFileDiff.MatchStatus.NO_MATCH)
    
    with open(file_name) as f:
        file_lines = f.readlines()[match_start_line-1:match_start_line-1 + len(search_lines_with_type) + PATCH_LENGTH_BUFFER]
    
    removed_diffs = []
    added_diffs = []
    context_diffs = []

    patch_line_type_to_list = {
        parse.natureOfChange.ADDED : added_diffs,
        parse.natureOfChange.REMOVED : removed_diffs,
        parse.natureOfChange.CONTEXT : context_diffs
    }

    matched_file_lines = set()
    for patch_line in search_lines_with_type:
        stripped_patch_line = patch_line[1].strip()
        max_ratio = 0
        max_ratio_file_line = ""
        for file_line in file_lines:
            cur_ratio = Levenshtein.ratio(file_line.strip(), stripped_patch_line)
            if cur_ratio > max_ratio:
                max_ratio = cur_ratio
                max_ratio_file_line = file_line.strip()
            if cur_ratio == 1:
                break
        if max_ratio == 1:
            matched_file_lines.add(max_ratio_file_line) 
        elif max_ratio > LEVENSHTEIN_RATIO:
            matched_file_lines.add(max_ratio_file_line) 

            diff_tokens = {}
            
            for token_type in token_diff_types:
                diff_tokens[token_type] = token_type_to_func[token_type](
                    patch_line = stripped_patch_line, file_line = max_ratio_file_line)

            line_diff_obj = Diff.LineDiff(
                patch_line = stripped_patch_line,
                file_line = max_ratio_file_line,
                is_missing = False,
                diff_tokens = diff_tokens,
                match_ratio = max_ratio,
            )
            patch_line_type_to_list[patch_line[0]].append(line_diff_obj)
        else:
            print(stripped_patch_line)
            print(file_lines)
            missing_diff = Diff.LineDiff(stripped_patch_line)
            patch_line_type_to_list[patch_line[0]].append(missing_diff)

    additional_lines = []
    for line in file_lines:
        if line.strip() not in matched_file_lines:
            additional_lines.append(line.strip())
                
    return Diff(
        match_status=Diff.MatchStatus.MATCH_FOUND,
        removed_diffs=removed_diffs,
        added_diffs=added_diffs,
        context_diffs=context_diffs,
        additional_lines=additional_lines
    )

# Testing
# patch_file = parse.PatchFile("../patches/CVE-2014-8172.patch")
# patch_file.getPatch()
# diff_obj = find_diffs(patch_file.patches[0]._lines, "../../msm-3.10/fs/file_table.c", 
#     try_already_applied=True, retry_obj=Retry(2,100), 
#     token_diff_types=[Diff.LineDiff.TokenDiffType.PLAINTEXT, Diff.LineDiff.TokenDiffType.C])
# print(diff_obj.match_status)
# print(diff_obj.removed_diffs)
# print(diff_obj.added_diffs)
# print(diff_obj.context_diffs)
# print(diff_obj.additional_lines)
# for obj in diff_obj.context_diffs:
#     print(obj.patch_line)
#     print(obj.diff_tokens[Diff.LineDiff.TokenDiffType.C])