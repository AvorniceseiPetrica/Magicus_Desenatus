from pathlib import Path

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QPainter

from models.objects.tile import TileType
from models.objects.world import World
from presentation.renderers.decal_cache import DecalCache
from presentation.renderers.renderer import Renderer

_TILE_SIZE = 48
_SPRITES_ROOT = Path(__file__).resolve().parents[2] / "models" / "sprites"

_TILE_COLORS = {
    TileType.FLOOR: QColor("#2a2a33"),
    TileType.WALL: QColor("#5a5a70"),
    TileType.CHASM: QColor("#e5e5e5"),
}

_TILE_SPRITES = {
    TileType.FLOOR: "tiles/floor.png",
    TileType.WALL:  "tiles/wall.png",
    TileType.CHASM: "tiles/chasm.png",
}
assert set(_TILE_SPRITES) == set(TileType)


class WorldRenderer(Renderer):
    def __init__(self, decals: DecalCache | None = None):
        self._decals = decals or DecalCache(_SPRITES_ROOT)

    def render(self, painter: QPainter, scene: World) -> None:
        painter.fillRect(painter.viewport(), QColor("#1e1e24"))

        # map
        painter.setPen(QColor("#3a3a46"))
        for gy, row in enumerate(scene.map):
            for gx, tile in enumerate(row):
                rect = QRect(gx * _TILE_SIZE, gy * _TILE_SIZE, _TILE_SIZE, _TILE_SIZE)
                pixmap = self._decals.get(_TILE_SPRITES[tile])
                if pixmap:
                    painter.drawPixmap(rect, pixmap)
                else:
                    painter.fillRect(rect, _TILE_COLORS[tile])
                    painter.drawRect(rect)

        # entities
        for e in scene.entities:
            rect = QRect(e.x * _TILE_SIZE + 2, e.y * _TILE_SIZE + 2, _TILE_SIZE - 4, _TILE_SIZE - 4)
            pixmap = self._decals.get(e.decal)
            if pixmap:
                painter.drawPixmap(rect, pixmap)
            else:
                painter.fillRect(rect, QColor("#4da6ff" if e.is_player else "#e05555"))
                painter.setPen(Qt.white)
                painter.drawText(rect, Qt.AlignCenter, e.name[0])
            painter.setPen(Qt.white)
            painter.drawText(rect.adjusted(0, 0, 0, -2), Qt.AlignBottom | Qt.AlignHCenter,
                             f"{e.hp}hp")

        # HUD
        painter.setPen(Qt.white)
        painter.drawText(8, scene.height * _TILE_SIZE + 24, f"Turn {scene.turn}   (Esc: menu)")
