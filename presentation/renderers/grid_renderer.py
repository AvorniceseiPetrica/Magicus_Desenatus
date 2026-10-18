from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor

from models.objects.grid import Grid
from models.objects.scene import Scene
from presentation.renderers.renderer import Renderer



class GridRenderer(Renderer):
    def __init__(self, spell_grid:Grid, cell_size = 60, padding: int = 10):
        self.cell_size = cell_size
        self.padding = padding
        self.spell_grid = spell_grid
        self.offset_x: int = 0
        self.offset_y: int = 0


    def render(self, painter: QPainter, scene: Scene) -> None:
        # linii între noduri vizitate
        if len(self.spell_grid.visited) > 1:
            painter.setPen(QPen(QColor("#4da6ff"), 2))
            for a, b in zip(self.spell_grid.visited, self.spell_grid.visited[1:]):
                painter.drawLine(self._to_screen(*a), self._to_screen(*b))

        # noduri
        for y in range(self.spell_grid.height):
            for x in range(self.spell_grid.width):
                pos = self._to_screen(x, y)
                if (x, y) in self.spell_grid.visited:
                    painter.setBrush(QColor("white"))
                else:
                    painter.setBrush(QColor("#3a3a46"))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(pos, 8, 8)

    def _to_screen(self, x: int, y: int) -> QPoint:
        return QPoint(
            self.offset_x + self.padding + x * self.cell_size,
            self.offset_y + self.padding + y * self.cell_size
        )


