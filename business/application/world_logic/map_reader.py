from models.objects.tile import TileType

# Each tile is written as a short code; tiles in a row are separated by spaces.
_TILE_CODES = {
    "EMP": TileType.EMPTY,
    "FL1": TileType.FLOOR_LIGHT_1,
    "FL2": TileType.FLOOR_LIGHT_2,
    "FD1": TileType.FLOOR_DARK_1,
    "FD2": TileType.FLOOR_DARK_2,
    "FD3": TileType.FLOOR_DARK_3,
    "WAL": TileType.WALL,
    "CHA": TileType.CHASM,
}
assert set(_TILE_CODES.values()) == set(TileType), "every TileType needs a code in _TILE_CODES"


def map_from_text(rows: list[str]) -> list[list[TileType]]:
    tiles = []
    for y, row in enumerate(rows):
        line = []
        for x, code in enumerate(row.split()):
            if code not in _TILE_CODES:
                raise ValueError(f"unknown tile code {code!r} at x={x}, y={y}")
            line.append(_TILE_CODES[code])
        tiles.append(line)
    return tiles

_SYMBOLS = {tile: code for code, tile in _TILE_CODES.items()}


def map_to_text(tiles: list[list[TileType]]) -> list[str]:
    return [" ".join(_SYMBOLS[t] for t in row) for row in tiles]
