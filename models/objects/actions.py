# models/objects/actions.py
from dataclasses import dataclass
from typing import Union
from models.objects.elements import AffinityType

Pos = tuple[int, int]


@dataclass(frozen=True)
class CastStarted:    caster_id: str; affinity: AffinityType


@dataclass(frozen=True)
class CastFizzled:    caster_id: str; reason: str


@dataclass(frozen=True)
class ManaChanged:    entity_id: str; delta: int


@dataclass(frozen=True)
class HpChanged:      entity_id: str; delta: int


@dataclass(frozen=True)
class EntityMoved:    entity_id: str; src: Pos; dst: Pos


@dataclass(frozen=True)
class ProjectileMoved: affinity: AffinityType; src: Pos; dst: Pos


@dataclass(frozen=True)
class AoeReleased:    affinity: AffinityType; center: Pos; tiles: tuple[Pos, ...]


@dataclass(frozen=True)
class EntityDied:     entity_id: str


Action = Union[CastStarted, CastFizzled, ManaChanged, HpChanged,
EntityMoved, ProjectileMoved, AoeReleased, EntityDied]
ActionList = list[Action]
