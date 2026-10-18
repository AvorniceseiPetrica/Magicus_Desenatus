from dataclasses import dataclass
import settings


@dataclass(frozen=True)
class Layout:
    tile: int
    view_cols: float  # câte coloane încap în lățimea ferestrei (fracționar)
    hud_y: int

def compute_layout(width: int, height: int) -> Layout:
    game_h = max(1, height - settings.HUD_HEIGHT)
    tile = max(1, game_h // settings.VIEW_ROWS)
    hud_y = tile * settings.VIEW_ROWS
    return Layout(tile, width / tile, hud_y)