from enum import Enum, auto


class Command(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    CONFIRM = auto()
    CANCEL = auto()
