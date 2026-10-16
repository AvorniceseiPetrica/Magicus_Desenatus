from pathlib import Path
from models.objects.entity import EntityState

# --- gameplay: nu depinde de fereastră ---
GRID_COLUMNS = 25
GRID_ROWS = 15

# --- layout ---
HUD_ROWS = 1               # rânduri de tile rezervate sub hartă
WINDOWED_TILE_SIZE = 48    # mărimea tile-ului când rulează în fereastră
MIN_TILE_SIZE = 32         # sub asta fereastra nu mai poate fi micșorată
FULLSCREEN = False

# --- animații (ms) ---
MOVE_MS = 150
FRAME_MS = {
    EntityState.IDLE: 300,
    EntityState.MOVE: 75,
    EntityState.ATTACK: 100,
    EntityState.HURT: 100,
}

# --- spell grid ---
SPELL_CELL_SIZE = 60
SPELL_PADDING = 10

SPRITES_ROOT = Path(__file__).resolve().parent / "models" / "sprites"