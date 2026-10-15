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
            self.map = [[TileType.FLOOR] * self.width for _ in range(self.height)]
        else:
            self.height = len(self.map)
            self.width = len(self.map[0])
            if any(len(row) != self.width for row in self.map):
                raise ValueError("map must be rectangular")