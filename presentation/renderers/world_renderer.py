from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QPainter
from models.objects.world import World
from presentation.renderers.decal_cache import DecalCache
from presentation.renderers.renderer import Renderer

TILE = 48


class WorldRenderer(Renderer):
    def __init__(self, decals: DecalCache | None = None):
        self._decals = decals or DecalCache()

    def render(self, painter: QPainter, scene: World) -> None:
        painter.fillRect(painter.viewport(), QColor("#1e1e24"))

        # grid
        painter.setPen(QColor("#3a3a46"))
        for gx in range(scene.width):
            for gy in range(scene.height):
                painter.drawRect(gx * TILE, gy * TILE, TILE, TILE)

        # entities
        for e in scene.entities:
            rect = QRect(e.x * TILE + 2, e.y * TILE + 2, TILE - 4, TILE - 4)
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
        painter.drawText(8, scene.height * TILE + 24, f"Turn {scene.turn}   (Esc: menu)")
