from enum import Enum

class Direction(Enum):
    LEFT =(-1,  0)
    RIGHT=( 1,  0)
    UP   =( 0, -1)
    DOWN =( 0,  1)