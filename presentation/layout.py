from dataclasses import dataclass
import settings


@dataclass(frozen=True)
class Layout:
    tile: int
    ox: int  # offset-ul hărții, pentru centrare
    oy: int


def compute_layout(width: int, height: int) -> Layout:
    rows = settings.GRID_ROWS + settings.HUD_ROWS
    tile = max(1, min(width // settings.GRID_COLUMNS, height // rows))
    return Layout(
        tile,
        (width - tile * settings.GRID_COLUMNS) // 2,
        (height - tile * rows) // 2,
    )