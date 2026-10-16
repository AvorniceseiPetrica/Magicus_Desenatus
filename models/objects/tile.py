from dataclasses import dataclass
from enum import Enum, auto


class TileType(Enum):
    EMPTY = auto()
    FLOOR_LIGHT_1 = auto()
    FLOOR_LIGHT_2 = auto()
    FLOOR_DARK_1 = auto()
    FLOOR_DARK_2 = auto()
    FLOOR_DARK_3 = auto()
    WALL = auto()
    CHASM = auto()

    @property
    def props(self) -> "TileProperties":
        return TILE_PROPS[self]


@dataclass(frozen=True)
class TileProperties:
    walkable: bool
    deadly: bool = False


TILE_PROPS = {
    TileType.EMPTY: TileProperties(walkable=True),
    TileType.FLOOR_LIGHT_1: TileProperties(walkable=True),
    TileType.FLOOR_LIGHT_2: TileProperties(walkable=True),
    TileType.FLOOR_DARK_1: TileProperties(walkable=True),
    TileType.FLOOR_DARK_2: TileProperties(walkable=True),
    TileType.FLOOR_DARK_3: TileProperties(walkable=True),
    TileType.WALL:  TileProperties(walkable=False),
    TileType.CHASM: TileProperties(walkable=True, deadly=True),
}

assert set(TILE_PROPS) == set(TileType), "every TileType needs an entry in TILE_PROPS"

WALKABLE = frozenset({
    TileType.FLOOR_LIGHT_1, TileType.FLOOR_LIGHT_2,
    TileType.FLOOR_DARK_1, TileType.FLOOR_DARK_2, TileType.FLOOR_DARK_3,
})
BLOCKS_SPELLS = frozenset({TileType.WALL, TileType.EMPTY})