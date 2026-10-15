import random
from models.objects.tile import TileType

_FLOORS = [TileType.FLOOR_LIGHT_1, TileType.FLOOR_LIGHT_2,
           TileType.FLOOR_DARK_1, TileType.FLOOR_DARK_2, TileType.FLOOR_DARK_3]


def generate_map(width: int, height: int, seed: int,
                   wall_chance: float = 0.2) -> list[list[TileType]]:
    rng = random.Random(seed)
    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            on_border = x in (0, width - 1) or y in (0, height - 1)
            if on_border or rng.random() < wall_chance:
                row.append(TileType.WALL)
            else:
                row.append(rng.choice(_FLOORS))
        tiles.append(row)
    return tiles