from PyQt5.QtGui import QPainter
from models.objects.menu import Menu
from presentation.renderers.renderer import Renderer


class MenuRenderer(Renderer):
    def render(self, painter: QPainter, scene: Menu) -> None:
        painter.drawText(40, 40, scene.title)
        for i, option in enumerate(scene.options):
            prefix = "> " if i == scene.selected else "  "
            painter.drawText(40, 80 + i * 24, prefix + option)
