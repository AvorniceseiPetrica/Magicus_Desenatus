from dataclasses import dataclass
from enum import Enum, auto


class TileType(Enum):
    FLOOR = auto()
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
    TileType.FLOOR: TileProperties(walkable=True),
    TileType.WALL:  TileProperties(walkable=False),
    TileType.CHASM: TileProperties(walkable=True, deadly=True),
}

assert set(TILE_PROPS) == set(TileType), "every TileType needs an entry in TILE_PROPS"