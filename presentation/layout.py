from dataclasses import dataclass
import settings


@dataclass(frozen=True)
class Layout:
    tile: int
    view_cols: float  # câte coloane încap în lățimea ferestrei (fracționar)
    hud_y: int
    hud_height: int
    spell_cell_size: int
    spell_panel_width: int


def compute_layout(width: int, height: int) -> Layout:
    hud_height = max(settings.MIN_HUD_HEIGHT, int(height * settings.HUD_RATIO))
    game_h = max(1, height - hud_height)
    tile = max(1, game_h // settings.VIEW_ROWS)
    hud_y = tile * settings.VIEW_ROWS
    # grila 5x5: padding + 4*cell + padding = hud_height - margine
    # vrem ca grila să ocupe ~90% din hud_height
    usable = int((hud_height - 2 * settings.SPELL_PADDING) * 0.9)
    spell_cell_size = max(20, usable // 4)
    spell_panel_width = max(settings.MIN_SPELL_PANEL_WIDTH, int(width * settings.SPELL_PANEL_RATIO))

    return Layout(tile, width / tile, hud_y, hud_height, spell_cell_size, spell_panel_width)