from dataclasses import dataclass, field
from models.objects.entity import Entity
from models.objects.scene import Scene
from models.objects.tile import TileType


@dataclass
class World(Scene):
    width: int = 25
    height: int = 15
    entities: list[Entity] = field(default_factory=list)
    turn: int = 1
    map: list[list[TileType]] = field(default_factory=list)

    def __post_init__(self):
        if not self.map:
            self.map = [[TileType.FLOOR] * self.height for _ in range(self.width)]
        else:
            self.width = len(self.map)
            self.height = len(self.map[0])
            if any(len(column) != self.height for column in self.map):
                raise ValueError("map must be rectangular")
