from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QPainter

from models.objects.tile import TileType
from models.objects.world import World
from presentation.renderers.decal_cache import DecalCache
from presentation.renderers.renderer import Renderer

TILE_SIZE = 48

TILE_COLORS = {
    TileType.FLOOR: QColor("#2a2a33"),
    TileType.WALL: QColor("#5a5a70"),
    TileType.CHASM: QColor("#e5e5e5"),
}


class WorldRenderer(Renderer):
    def __init__(self, decals: DecalCache | None = None):
        self._decals = decals or DecalCache()

    def render(self, painter: QPainter, scene: World) -> None:
        painter.fillRect(painter.viewport(), QColor("#1e1e24"))

        # tiles
        painter.setPen(QColor("#3a3a46"))
        for gy, row in enumerate(scene.tiles):
            for gx, tile in enumerate(row):
                painter.fillRect(gx * TILE_SIZE, gy * TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_COLORS[tile])
                painter.drawRect(gx * TILE_SIZE, gy * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # entities
        for e in scene.entities:
            rect = QRect(e.x * TILE_SIZE + 2, e.y * TILE_SIZE + 2, TILE_SIZE - 4, TILE_SIZE - 4)
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
        painter.drawText(8, scene.height * TILE_SIZE + 24, f"Turn {scene.turn}   (Esc: menu)")
