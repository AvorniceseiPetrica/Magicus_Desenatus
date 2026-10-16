from dataclasses import dataclass
from enum import Enum, auto
from models.objects.elements import AffinityType, Direction


class Command(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    CONFIRM = auto()
    CANCEL = auto()


class SpellKind(Enum):
    SELF = auto();
    DIRECTIONAL = auto();
    DIRECTIONAL_AOE = auto()


@dataclass(frozen=True)
class SpellRequest:
    affinity: AffinityType
    kind: SpellKind
    directions: tuple[Direction, ...]


Input = Command | SpellRequest
