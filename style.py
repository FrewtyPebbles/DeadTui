from enum import Enum

class BorderStyle(Enum):
    SOLID = 0
    THIN_SOLID = 1
    DASHED = 2
    THIN_DASHED = 3
    DOTTED = 4
    THIN_DOTTED = 5
    THICK = 6

class FitType(Enum):
    SNUG = 0
    STATIC = 1
    STATIC_SNUG = 2
    DEFAULT = 3