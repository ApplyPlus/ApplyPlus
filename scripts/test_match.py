import diff_match_patch as dmp_module
import patchParser as parse 
from enum import Enum
import Levenshtein
from pygments.lexers import CLexer, CppLexer, CSharpLexer, JavaLexer, get_lexer_for_filename

dmp = dmp_module.diff_match_patch()
LEVENSHTEIN_RATIO = 0.8

"""
The purpose of this variable is because (start of matched code + patch length)
does not always contain the entire patch, so our matched code is the section from
(start of matched code) to (start of matched code + patch length + PATCH_LENGTH_BUFFER)
"""
PATCH_LENGTH_BUFFER = 10

class Retry():
    def __init__(self, retry_times, retry_interval):
        self.retry_times = retry_times
        self.retry_interval = retry_interval

class Diff():
    class LineDiff():
        class LanguageSpecificDiff():
            class Language(Enum):
                NOT_SUPPORTED = -1
                C = 0
                CPP = 1
                CSHARP = 2
                JAVA = 3
            
            lexer_to_language = {
                CLexer : Language.C,
                CppLexer : Language.CPP,
                CSharpLexer : Language.CSHARP,
                JavaLexer : Language.JAVA
            }

            def __init__(self, language = Language.NOT_SUPPORTED, patch_tokens = [], file_tokens=[], diff_tokens=[]):
                self.language = language
                self.patch_tokens = patch_tokens
                self.file_tokens = file_tokens
                self.diff_tokens = diff_tokens

        def __init__(self, patch_line, file_line="", is_missing=True, plaintext_diff = [], 
            language_specific_diff = LanguageSpecificDiff(), match_ratio=-1,
            function_for_patch="", file_line_number=-1):

            self.patch_line = patch_line
            self.file_line = file_line
            self.is_missing = is_missing
            self.plaintext_diff = plaintext_diff
            self.language_specific_diff = language_specific_diff
            self.match_ratio = match_ratio
            self.function_for_patch = function_for_patch
            self.file_line_number = file_line_number 

    class MatchStatus(Enum):
        NO_MATCH = 0
        MATCH_FOUND = 1

    def __init__(self, match_status, removed_diffs = [], added_diffs = [], context_diffs = [], additional_lines = [], function_for_patch=""):
        self.match_status = match_status
        self.removed_diffs = removed_diffs
        self.added_diffs = added_diffs
        self.context_diffs = context_diffs
        self.additional_lines = additional_lines
        self.function_for_patch = function_for_patch

"""
See docs for output format:
https://github.com/google/diff-match-patch/wiki/API
"""
def calculate_plaintext_diff(patch_line, file_line):
    diff_tokens = dmp.diff_main(patch_line, file_line)
    dmp.diff_cleanupSemantic(diff_tokens)
    return diff_tokens

def calculate_language_diff(patch_line, file_line, file_name):
    lexer = get_lexer_for_filename(file_name)
    language = Diff.LineDiff.LanguageSpecificDiff.lexer_to_language[type(lexer)]

    if language == Diff.LineDiff.LanguageSpecificDiff.Language.NOT_SUPPORTED:
        return Diff.LineDiff.LanguageSpecificDiff()

    patch_tokens = []
    token_stream = lexer.get_tokens(patch_line)
    for token in token_stream:
        patch_tokens.append(token)

    file_tokens = []
    token_stream = lexer.get_tokens(file_line)
    for token in token_stream:
       file_tokens.append(token)
    
    diff_tokens = list(set(patch_tokens) - set(file_tokens))

    return Diff.LineDiff.LanguageSpecificDiff(
        language=language,
        patch_tokens=patch_tokens,
        file_tokens=file_tokens,
        diff_tokens=diff_tokens
    )

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
        else:
            search_location = cur_char

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
        return file_str[:char_match_loc+1].count("\n") + 1
    else:
        return -1

def get_file_with_patch(patch_lines):
    search_lines = []
    for line in patch_lines:
        if line[0] != parse.natureOfChange.REMOVED:
            search_lines.append(line)
    
    return search_lines

def get_file_without_patch(patch_lines):
    search_lines = []
    for line in patch_lines:
        if line[0] != parse.natureOfChange.ADDED:
            search_lines.append(line)
    
    return search_lines

# Returns an object containing information about the difference between a file and a patch
def find_diffs(patch_obj, file_name, retry_obj=None, match_distance=3000):
    dmp.Match_Distance = match_distance 
    function_for_patch, patch_lines = patch_obj._lines[0][1], patch_obj._lines[1:]
    line_number = patch_obj._lineschanged[2] 

    search_lines_with_type = get_file_with_patch(patch_lines)
    search_lines_without_type = [line[1] for line in search_lines_with_type]
    match_start_line = fuzzy_search(search_lines_without_type, file_name, line_number, retry_obj)

    if match_start_line == -1:
        search_lines_with_type = get_file_without_patch(patch_lines)
        search_lines_without_type = [line[1] for line in search_lines_with_type]
        match_start_line = fuzzy_search(search_lines_without_type, file_name, line_number, retry_obj)
    
    if match_start_line == -1:
        return Diff(Diff.MatchStatus.NO_MATCH)
    
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
    for idx, patch_line in enumerate(search_lines_with_type):
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

            plaintext_diff = calculate_plaintext_diff(stripped_patch_line, max_ratio_file_line)

            language_specific_diff = calculate_language_diff(stripped_patch_line, max_ratio_file_line, file_name)

            line_diff_obj = Diff.LineDiff(
                patch_line = stripped_patch_line,
                file_line = max_ratio_file_line,
                file_line_number = match_start_line + idx + 1,
                is_missing = False,
                plaintext_diff = plaintext_diff,
                language_specific_diff=language_specific_diff,
                match_ratio = max_ratio,
                function_for_patch = function_for_patch,
            )
            patch_line_type_to_list[patch_line[0]].append(line_diff_obj)
        else:
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
        additional_lines=additional_lines,
        function_for_patch=function_for_patch
    )

# Testing
# patch_file = parse.PatchFile("../patches/CVE-2014-9322.patch")
# patch_file.getPatch()
# diff_obj = find_diffs(patch_file.patches[0], "../../msm-3.10/arch/x86/include/asm/page_32_types.h",
#     retry_obj=Retry(2,100), match_distance=3000)
# print(diff_obj.match_status)
# print(diff_obj.removed_diffs)
# print(diff_obj.added_diffs)
# print(diff_obj.context_diffs)
# print(diff_obj.additional_lines)
# for x in diff_obj.context_diffs:
#     print(x.function_for_patch)
#     print(x.file_line_number)
#     print(x.file_line)