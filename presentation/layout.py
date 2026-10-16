from dataclasses import dataclass
import settings


@dataclass(frozen=True)
class Layout:
    tile: int
    view_cols: float  # câte coloane încap în lățimea ferestrei (fracționar)


def compute_layout(width: int, height: int) -> Layout:
    tile = max(1, height // (settings.VIEW_ROWS + settings.HUD_ROWS))
    return Layout(tile, width / tile)