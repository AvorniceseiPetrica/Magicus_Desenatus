from dataclasses import dataclass, field
from enum import Enum, auto


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

    def set_state(self, state: EntityState) -> None:
        self.state = state
        self.state_seq += 1
