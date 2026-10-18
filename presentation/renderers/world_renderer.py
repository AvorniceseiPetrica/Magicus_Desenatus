from math import floor, ceil
from pathlib import Path

from PyQt5.QtCore import QRect, Qt, QPointF, QRectF
from PyQt5.QtGui import QColor, QPainter, QPen

import settings
from models.objects.elements import AffinityType
from models.objects.entity import EntityState
from models.objects.frame import EffectKind
from models.objects.grid import Grid
from models.objects.tile import TileType
from models.objects.world import World
from presentation.camera import camera_origin
from presentation.layout import compute_layout
from presentation.renderers.decal_cache import DecalCache
from presentation.renderers.grid_renderer import GridRenderer
from presentation.renderers.renderer import Renderer

import time

from settings import SPRITES_ROOT, MOVE_MS, FRAME_MS

_TILE_SPRITES = {
    TileType.EMPTY: "other/empty.png",
    TileType.FLOOR_LIGHT_1: "tiles/level1/floor_light_1.png",
    TileType.FLOOR_LIGHT_2: "tiles/level1/floor_light_2.png",
    TileType.FLOOR_DARK_1: "tiles/level1/floor_dark_1.png",
    TileType.FLOOR_DARK_2: "tiles/level1/floor_dark_2.png",
    TileType.FLOOR_DARK_3: "tiles/level1/floor_dark_3.png",
    TileType.WALL: "tiles/level1/wall.png",
    TileType.CHASM: "tiles/level1/chasm.png",
}
assert set(_TILE_SPRITES) == set(TileType)

_AFFINITY_COLORS = {AffinityType.FIRE: "#ff7a2f", AffinityType.WATER: "#3fa9ff",
                    AffinityType.HOLY: "#ffe680", AffinityType.DARKNESS: "#9b59d0"}


class WorldRenderer(Renderer):
    def __init__(self, decals: DecalCache | None = None):
        self._decals = decals or DecalCache(SPRITES_ROOT)
        self._grid_renderer = GridRenderer(Grid())
        self._slides: dict[int, tuple] = {}
        self._latched: dict[int, tuple] = {}

    @property
    def spell_grid(self) -> Grid:
        return self._grid_renderer.spell_grid

    def render(self, painter: QPainter, scene: World) -> None:
        view = painter.viewport()
        lay = compute_layout(view.width(), view.height())
        t = lay.tile
        vc, vr = lay.view_cols, settings.VIEW_ROWS

        painter.fillRect(view, QColor("#1e1e24"))

        font = painter.font()
        font.setPixelSize(max(8, t // 3))
        painter.setFont(font)

        # stare animații + poziții desenate (o singură dată pe cadru)
        now = time.monotonic() * 1000
        live = {id(e) for e in scene.entities}
        self._slides = {k: v for k, v in self._slides.items() if k in live}
        self._latched = {k: v for k, v in self._latched.items() if k in live}
        pos = {id(e): self._drawn_pos(e, now) for e in scene.entities}

        # cameră, în unități de tile
        player = next((e for e in scene.entities if e.is_player), None)
        fx, fy = pos[id(player)] if player else ((scene.width - 1) / 2, (scene.height - 1) / 2)
        cam_x = camera_origin(fx, vc, scene.width)
        cam_y = camera_origin(fy, vr, scene.height)

        def to_px(gx: float, gy: float) -> tuple[int, int]:
            return round((gx - cam_x) * t), round((gy - cam_y) * t)

        game_width = view.width() - settings.SPELL_PANEL_WIDTH
        painter.save()
        painter.setClipRect(0, 0, game_width, lay.hud_y)

        # map: doar dalele vizibile
        painter.setPen(QColor("#3a3a46"))
        for gy in range(max(0, floor(cam_y)), min(scene.height, ceil(cam_y + vr))):
            for gx in range(max(0, floor(cam_x)), min(scene.width, ceil(cam_x + vc))):
                rect = QRect(*to_px(gx, gy), t, t)
                pixmap = self._decals.get(_TILE_SPRITES[scene.map[gy][gx]])
                if pixmap:
                    painter.drawPixmap(rect, pixmap)
                else:
                    painter.fillRect(rect, QColor("#ff00ff"))  # magenta = missing sprite
                    painter.drawRect(rect)

        # entities
        m = t // 24
        for e in scene.entities:
            x, y = to_px(*pos[id(e)])
            rect = QRect(x + m, y + m, t - 2 * m, t - 2 * m)
            pixmap = self._decals.get(self._frame(e, now))
            if pixmap:
                painter.drawPixmap(rect, pixmap)
            else:
                painter.fillRect(rect, QColor("#4da6ff" if e.is_player else "#e05555"))
                painter.setPen(Qt.white)
                painter.drawText(rect, Qt.AlignCenter, e.name[0])
            painter.setPen(Qt.white)
            painter.drawText(rect.adjusted(0, 0, 0, -2), Qt.AlignBottom | Qt.AlignHCenter,
                             f"{e.hp}hp")

        painter.restore()

        painter.setPen(QPen(QColor("#8b6914"), 3))
        painter.drawLine(0, lay.hud_y, view.width(), lay.hud_y)  # border jos
        painter.drawLine(game_width, 0, game_width, lay.hud_y)  # border dreapta

        # HUD, sub viewport
        painter.fillRect(0, lay.hud_y, view.width(), view.height() - lay.hud_y, QColor("#3b2008"))
        painter.fillRect(game_width + 3, 0, view.width() - game_width - 3, lay.hud_y, QColor("#3b2008"))

        painter.setPen(Qt.white)
        painter.drawText(8, lay.hud_y + t // 2, f"Turn {scene.turn}   (Esc: menu)")

    def _drawn_pos(self, e, now):
        """Entity position in tile units (floats while sliding) and whether it is moving."""
        fx, fy, tx, ty, t0 = self._slides.get(id(e), (e.x, e.y, e.x, e.y, now - MOVE_MS))
        k = min(1.0, (now - t0) / MOVE_MS)
        cx, cy = fx + (tx - fx) * k, fy + (ty - fy) * k
        if (e.x, e.y) != (tx, ty):  # moved since last frame: restart from where it is drawn now
            fx, fy, tx, ty, t0 = cx, cy, e.x, e.y, now
            k = 0.0
        self._slides[id(e)] = (fx, fy, tx, ty, t0)
        return cx, cy

    def _frame(self, e, now):
        key = (e.state, e.state_seq)
        latched = self._latched.get(id(e))
        if latched is None or latched[0] != key:  # new action: restart its animation
            latched = (key, now)
            self._latched[id(e)] = latched
        frames = e.sprites.get(e.state, ())
        if e.state is not EntityState.IDLE and frames:
            i = int((now - latched[1]) // FRAME_MS[e.state])
            if i < len(frames):  # one-shot still playing
                return frames[i]
        idle = e.sprites.get(EntityState.IDLE, ())
        return idle[int(now // FRAME_MS[EntityState.IDLE]) % len(idle)] if idle else ""

    def _effect(self, painter, fx, t, to_px):
        px, py = to_px(fx.x, fx.y)  # colțul stânga-sus al tile-ului, în pixeli
        cx, cy = px + t / 2, py + t / 2
        color = QColor(_AFFINITY_COLORS.get(fx.affinity, "#ffffff"))
        if fx.kind is EffectKind.PROJECTILE:
            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.drawEllipse(QPointF(cx, cy), t * 0.17, t * 0.17)
        elif fx.kind is EffectKind.BURST:
            color.setAlphaF(0.6 * (1 - fx.progress))
            painter.fillRect(QRectF(px, py, t, t), color)
        elif fx.kind is EffectKind.FLASH:
            color.setAlphaF(1 - fx.progress)
            painter.setPen(color)
            painter.setBrush(Qt.NoBrush)
            r = t / 2 * (0.6 + fx.progress)
            painter.drawEllipse(QPointF(cx, cy), r, r)
        elif fx.kind is EffectKind.TEXT:
            painter.setPen(Qt.white)
            painter.drawText(QRectF(px - t / 2, py, 2 * t, t / 2), Qt.AlignCenter, fx.text)