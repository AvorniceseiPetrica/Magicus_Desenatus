from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QPainter, QFont, QPixmap

import settings
from models.objects.cutscene import Cutscene, CutsceneClearScreen, CutsceneImage, CutsceneTextBubble
from presentation.renderers.renderer import Renderer

FONT_HEIGHT_FRACTION = 0.035
FADE_IN_TIME_MS = 500

class CutsceneRenderer(Renderer):
    def __init__(self):
        self._cache: dict[str, QPixmap] = {}

    def _pixmap(self, folder: str, file: str) -> QPixmap:
        key = f"{folder}/{file}"
        if key not in self._cache:
            self._cache[key] = QPixmap(key)
        return self._cache[key]

    def render(self, painter: QPainter, scene: Cutscene) -> None:
        view = painter.viewport()
        painter.fillRect(view, Qt.black)
        painter.setRenderHints(QPainter.SmoothPixmapTransform |
                               QPainter.TextAntialiasing)

        scene.time_last_shown += settings.TICK_MS
        if(scene.index<len(scene.cutscene_objects) and scene.time_last_shown > scene.cutscene_objects[scene.index].delay):
            scene.index += 1
            scene.time_last_shown = 0

        last_clear = max((i for i, obj in enumerate(scene.cutscene_objects[:scene.index])
                          if isinstance(obj, CutsceneClearScreen)), default=-1)

        for obj in scene.cutscene_objects[last_clear + 1:scene.index]:
            if scene.cutscene_objects.index(obj) == scene.index-1:
                painter.setOpacity(min(1.0, scene.time_last_shown / FADE_IN_TIME_MS))

            if isinstance(obj, CutsceneImage):
                self._draw_image(painter, view, scene.cutscene_dir, obj)
            elif isinstance(obj, CutsceneTextBubble):
                self._draw_bubble(painter, view, obj)

            painter.setOpacity(1.0)

    def _draw_image(self, painter: QPainter, view: QRect,
                    folder: str, obj: CutsceneImage) -> None:
        pixmap = self._pixmap(folder, obj.path)
        if pixmap.isNull():
            return
        x = int(obj.position[0] * view.width())
        y = int(obj.position[1] * view.height())
        w = int(obj.width * view.width())
        h = int(pixmap.height() * w / pixmap.width())   # păstrează proporția
        painter.drawPixmap(QRect(x, y, w, h), pixmap)

    def _draw_bubble(self, painter: QPainter, view: QRect,
                     obj: CutsceneTextBubble) -> None:
        font = QFont(painter.font())
        font.setPixelSize(max(8, int(view.height() * FONT_HEIGHT_FRACTION)))
        painter.setFont(font)

        pad_x = font.pixelSize() // 2
        pad_y = font.pixelSize() // 3
        flags = Qt.AlignLeft | Qt.TextWordWrap

        x = int(obj.position[0] * view.width())
        y = int(obj.position[1] * view.height())
        w = int(obj.max_width * view.width())

        text_rect = painter.boundingRect(QRect(x, y, w, 4000), flags, obj.text)
        box = text_rect.adjusted(-pad_x, -pad_y, pad_x, pad_y)

        painter.fillRect(box, QColor(30, 30, 40, 230))
        painter.setPen(Qt.white)
        painter.drawRect(box)
        painter.drawText(text_rect, flags, obj.text)