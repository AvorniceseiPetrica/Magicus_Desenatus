# models/objects/frame.py
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
from models.objects.elements import AffinityType
from models.objects.entity import EntityState
from models.objects.scene import Scene
from models.objects.tile import TileType


class EffectKind(Enum):
    PROJECTILE = auto();
    BURST = auto();
    FLASH = auto();
    TEXT = auto()


@dataclass
class EntityView:
    id: str
    name: str
    x: float  # float: mid-slide positions
    y: float
    hp: int
    max_hp: int
    mana: int
    max_mana: int
    sprites: dict[EntityState, tuple[str, ...]]
    state: EntityState
    state_seq: int
    is_player: bool
    alpha: float = 1.0


@dataclass(frozen=True)
class Effect:
    kind: EffectKind
    x: float
    y: float
    progress: float  # 0..1
    affinity: Optional[AffinityType] = None
    text: str = ""


@dataclass
class WorldFrame(Scene):
    map: list[list[TileType]]
    entities: list[EntityView]
    effects: list[Effect] = field(default_factory=list)
    turn: int = 1
    awaiting_input: bool = False

    @property
    def width(self) -> int: return len(self.map[0])

    @property
    def height(self) -> int: return len(self.map)
