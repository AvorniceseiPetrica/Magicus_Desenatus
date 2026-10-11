from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QPainter
from models.objects.cutscene import Cutscene
from presentation.renderers.renderer import Renderer


class CutsceneRenderer(Renderer):
    def render(self, painter: QPainter, scene: Cutscene) -> None:
        view = painter.viewport()
        painter.fillRect(view, Qt.black)
        if not scene.lines:
            return

        box = QRect(40, view.height() - 160, view.width() - 80, 120)
        painter.fillRect(box, QColor(30, 30, 40, 230))
        painter.setPen(Qt.white)
        painter.drawRect(box)
        painter.drawText(box.adjusted(16, 16, -16, -16),
                         Qt.AlignLeft | Qt.TextWordWrap,
                         scene.lines[scene.index])

        painter.setPen(QColor("#aaaaaa"))
        painter.drawText(box.adjusted(0, 0, -12, -8), Qt.AlignRight | Qt.AlignBottom,
                         "Enter: next   Esc: skip")
