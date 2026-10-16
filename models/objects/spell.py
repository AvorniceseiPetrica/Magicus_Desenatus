from dataclasses import dataclass
from enum import Enum, auto
from models.objects.elements import AffinityType, Direction
from models.objects.entity import Entity


class PropagationType(Enum):
    SELF = auto();
    DIRECTIONAL = auto()


@dataclass(frozen=True)
class SpellAffinity:
    type: AffinityType


@dataclass(frozen=True)
class SpellPropagation:
    type: PropagationType
    directions: tuple[Direction, ...]
    aoe_at_end: bool = False


@dataclass(frozen=True)
class SpellCast:
    caster: Entity
    affinity: SpellAffinity
    propagation: SpellPropagation
