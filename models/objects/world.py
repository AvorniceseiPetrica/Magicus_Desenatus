from dataclasses import dataclass, field

import settings
from models.objects.entity import Entity
from models.objects.scene import Scene
from models.objects.tile import TileType, WALKABLE, BLOCKS_SPELLS


@dataclass
class World(Scene):
    width: int = settings.VIEW_COLUMNS
    height: int = settings.VIEW_ROWS
    entities: list[Entity] = field(default_factory=list)
    turn: int = 1
    map: list[list[TileType]] = field(default_factory=list)

    def __post_init__(self):
        if not self.map:
            self.map = [[TileType.FLOOR_LIGHT_1] * self.width for _ in range(self.height)]
        else:
            self.height = len(self.map)
            self.width = len(self.map[0])
            if any(len(row) != self.width for row in self.map):
                raise ValueError("map must be rectangular")

    @property
    def player(self) -> Entity | None:
        return next((e for e in self.entities if e.is_player), None)

    @property
    def enemies(self) -> list[Entity]:
        return [e for e in self.entities if not e.is_player]

    def get(self, entity_id: str) -> Entity | None:
        return next((e for e in self.entities if e.id == entity_id), None)

    def entity_at(self, x: int, y: int) -> Entity | None:
        return next((e for e in self.entities if e.x == x and e.y == y), None)

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def walkable(self, x: int, y: int) -> bool:  # for bodies
        return self.in_bounds(x, y) and self.map[y][x] in WALKABLE

    def flyable(self, x: int, y: int) -> bool:  # for projectiles / AOE
        return self.in_bounds(x, y) and self.map[y][x] not in BLOCKS_SPELLS

    def is_free(self, x: int, y: int) -> bool:  # walkable and unoccupied
        return self.walkable(x, y) and self.entity_at(x, y) is None