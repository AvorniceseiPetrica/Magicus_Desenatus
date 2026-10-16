from enum import Enum


class AffinityType(Enum):
    WATER = "water"
    FIRE = "fire"
    HOLY = "holy"
    DARKNESS = "darkness"


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
