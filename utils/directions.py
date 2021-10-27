from enum import Enum

class Direction(Enum):
    LEFT =(-1,  0)
    RIGHT=( 1,  0)
    UP   =( 0, -1)
    DOWN =( 0,  1)

    @classmethod
    def getDirection(self, dx: int, dy: int):
        if dx > 0:
            return Direction.RIGHT
        if dx < 0:
            return Direction.LEFT
        if dy > 0:
            return Direction.UP
        return Direction.DOWN