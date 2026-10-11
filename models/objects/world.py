from dataclasses import dataclass, field
from models.objects.entity import Entity
from models.objects.scene import Scene


@dataclass
class World(Scene):
    width: int = 10
    height: int = 10
    entities: list[Entity] = field(default_factory=list)
    turn: int = 1
