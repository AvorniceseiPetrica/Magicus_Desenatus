from dataclasses import dataclass
import settings

Rect = tuple[int, int, int, int]  # x, y, w, h în pixeli


@dataclass(frozen=True)
class Layout:
    tile: int
    view_cols: float  # câte coloane încap în lățimea ferestrei (fracționar)
    spell_panel_x: int  # marginea stângă a HUD-ului din dreapta
    spell_panel_width: int
    spell_cell_size: int
    grid_x: int  # originea grilei de desenat (stânga-sus, înainte de padding)
    grid_y: int
    # --- HUD dreapta: o singură coloană, toate pătratele au aceeași latură ---
    info_rect: Rect  # tura curentă + hint
    spell_slots: tuple[Rect, ...]  # de sus în jos
    confirm_rect: Rect
    reset_rect: Rect
    book_rect: Rect  # jos
    hud_font_px: int  # textul din HUD trebuie să încapă pe lățimea unui pătrat


def compute_layout(width: int, height: int) -> Layout:
    # harta ocupă toată fereastra; HUD-ul și grila sunt desenate peste ea
    tile = max(1, height // settings.VIEW_ROWS)

    # grila 5x5 rămâne deocamdată în stânga-jos: padding + 4*cell + padding
    spell_cell_size = settings.SPELL_CELL_SIZE
    grid_size = 2 * settings.SPELL_PADDING + 4 * spell_cell_size
    grid_x = settings.SPELL_PADDING
    grid_y = height - grid_size - settings.SPELL_PADDING

    panel_x, panel_w, info, slots, confirm, reset, book = _side_hud(width, height, tile)

    return Layout(tile, width / tile, panel_x, panel_w,
                  spell_cell_size, grid_x, grid_y,
                  info, slots, confirm, reset, book, max(8, info[2] // 5))


def _side_hud(width: int, height: int, tile: int):
    """Coloana din dreapta, de sus în jos: info | n sloturi | Confirm | Reset | ... | carte.
    Latura pătratelor se alege din înălțime; lățimea panoului = latura + 2 * margine."""
    m, gap, n = settings.HUD_MARGIN, settings.HUD_GAP, settings.SPELL_SLOTS

    info_h = 2 * (tile // 2)  # două rânduri de text
    top = m + info_h + gap

    # n sloturi + 2 butoane + carte = n + 3 pătrate;
    # gap între pătrate + câte un gap în plus între grupuri (sloturi | butoane | carte)
    squares = n + 3
    gaps = (squares - 1) * gap + 2 * gap
    side = max(1, (height - top - m - gaps) // squares)

    panel_w = side + 2 * m
    panel_x = width - panel_w
    x = panel_x + m  # coloana, lipită de marginea din dreapta (cu margine)

    info = (x, m, side, info_h)
    slots = tuple((x, top + i * (side + gap), side, side) for i in range(n))
    y = top + n * (side + gap) + gap
    confirm = (x, y, side, side)
    reset = (x, y + side + gap, side, side)
    book = (x, height - m - side, side, side)
    return panel_x, panel_w, info, slots, confirm, reset, book
