from models.objects.tile import TileType

_TILE_CHARS = {
    "#": TileType.WALL,
    ".": TileType.FLOOR,
    "~": TileType.CHASM
}


def map_from_text(rows: list[str]) -> list[list[TileType]]:
    tiles = []
    for y, row in enumerate(rows):
        line = []
        for x, ch in enumerate(row):
            if ch not in _TILE_CHARS:
                raise ValueError(f"unknown map character {ch!r} at x={x}, y={y}")
            line.append(_TILE_CHARS[ch])
        tiles.append(line)
    return tiles

_SYMBOLS = {tile: ch for ch, tile in _TILE_CHARS.items()}


def map_to_text(tiles: list[list[TileType]]) -> list[str]:
    return ["".join(_SYMBOLS[t] for t in row) for row in tiles]