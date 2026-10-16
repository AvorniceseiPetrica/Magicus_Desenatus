from dataclasses import dataclass, field
from enum import Enum, auto
from models.objects.elements import AffinityType
from uuid import uuid4


class EntityState(Enum):
    IDLE = auto()
    MOVE = auto()
    ATTACK = auto()
    HURT = auto()

@dataclass
class Entity:
    name: str
    x: int
    y: int
    hp: int = 3
    sprites: dict[EntityState, tuple[str, ...]] = field(default_factory=dict)
    is_player: bool = False
    state: EntityState = EntityState.IDLE
    state_seq: int = 0
    max_hp: int = 0                 # 0 = same as the starting hp
    mana: int = 10
    max_mana: int = 0               # 0 = same as the starting mana
    affinity: AffinityType = AffinityType.FIRE
    id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        self.max_hp = self.max_hp or self.hp
        self.max_mana = self.max_mana or self.mana

    def set_state(self, state: EntityState) -> None:
        self.state = state
        self.state_seq += 1
