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
    tiles: list[list[TileType]] = field(default_factory=list)

    def __post_init__(self):
        if not self.tiles:
            self.tiles = [[TileType.FLOOR] * self.width for _ in range(self.height)]
        else:
            self.height = len(self.tiles)
            self.width = len(self.tiles[0])
            if any(len(row) != self.width for row in self.tiles):
                raise ValueError("tiles must be rectangular")
