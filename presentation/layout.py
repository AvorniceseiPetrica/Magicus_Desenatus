from dataclasses import dataclass
import settings


@dataclass(frozen=True)
class Layout:
    tile: int
    view_cols: float  # câte coloane încap în lățimea ferestrei (fracționar)
    spell_panel_x: int  # marginea stângă a HUD-ului din dreapta
    spell_panel_width: int
    spell_cell_size: int
    grid_x: int  # originea grilei de desenat (stânga-sus, înainte de padding)
    grid_y: int


def compute_layout(width: int, height: int) -> Layout:
    # harta ocupă toată fereastra; HUD-ul și grila sunt desenate peste ea
    tile = max(1, height // settings.VIEW_ROWS)

    spell_panel_width = max(settings.MIN_SPELL_PANEL_WIDTH, int(width * settings.SPELL_PANEL_RATIO))
    spell_panel_x = width - spell_panel_width

    # grila 5x5 rămâne deocamdată în stânga-jos: padding + 4*cell + padding
    spell_cell_size = settings.SPELL_CELL_SIZE
    grid_size = 2 * settings.SPELL_PADDING + 4 * spell_cell_size
    grid_x = settings.SPELL_PADDING
    grid_y = height - grid_size - settings.SPELL_PADDING

    return Layout(tile, width / tile, spell_panel_x, spell_panel_width,
                  spell_cell_size, grid_x, grid_y)
