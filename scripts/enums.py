from enum import Enum


class CONTEXT_DECISION(Enum):
    DONT_RUN = 0
    RUN = 1


class SliceFields(Enum):
    FILEPATH = 0
    FUNCTION_NAME = 1
    VARIABLE_NAME = 2
    DEF = 3
    USE = 4
    DVARS = 5
    POINTERS = 6
    CFUNCS = 7


class Language(Enum):
    NOT_SUPPORTED = -1
    C = 0
    CPP = 1
    CSHARP = 2
    JAVA = 3


class MatchStatus(Enum):
    NO_MATCH = 0
    MATCH_FOUND = 1


class natureOfChange(Enum):
    ADDED = 1
    REMOVED = -1
    CONTEXT = 0
