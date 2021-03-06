number_of_tiles = 90

number_of_rows = 16
number_of_columns = 16

multiplicity = {
    'A':9,
    'B':2,
    'C':2,
    'D':5,
    'E':13,
    'F':2,
    'G':3,
    'H':4,
    'I':8,
    'J':1,
    'K':1,
    'L':4,
    'M':2,
    'N':5,
    'O':8,
    'P':2,
    'Q':1,
    'R':6,
    'S':5,
    'T':7,
    'U':4,
    'V':2,
    'W':2,
    'X':1,
    'Y':2,
    'Z':1,
    'BLANK':2,
    }

points_map = {
    'A':1,
    'B':4,
    'C':4,
    'D':2,
    'E':1,
    'F':4,
    'G':3,
    'H':3,
    'I':1,
    'J':10,
    'K':5,
    'L':2,
    'M':4,
    'N':2,
    'O':1,
    'P':4,
    'Q':10,
    'R':1,
    'S':1,
    'T':1,
    'U':2,
    'V':5,
    'W':4,
    'X':8,
    'Y':3,
    'Z':10,
    'BLANK':0,
}

wordfile = 'data/wordlist.txt'

TW = 1
DW = 2
TL = 3
DL = 4

modifiers = {
    (0, 3): TW,
    (0, 6): TL,
    (1, 2): DL,
    (1, 5): DW,
    (2, 1): DL,
    (2, 4): DL,
    (3, 0): TW,
    (3, 3): TL,
    (3, 7): DW,
    (4, 2): DL,
    (4, 6): DL,
    (5, 1): DW,
    (5, 5): TL,
    (6, 0): TL,
    (6, 4): DL,
    (7, 3): DW,
}
