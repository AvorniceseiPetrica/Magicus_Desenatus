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
        self.visible: bool = False  # apare la primul click dreapta

    @property
    def size(self) -> int:
        """Latura grilei în pixeli: padding + (n-1)*cell + padding."""
        return 2 * self.padding + (self.spell_grid.width - 1) * self.cell_size

    def place_at(self, cx: int, cy: int, max_x: int, max_y: int) -> None:
        """Centrează grila pe (cx, cy), dar o ține în dreptunghiul [0, max_x] x [0, max_y]."""
        s = self.size
        self.offset_x = min(max(cx - s // 2, 0), max(0, max_x - s))
        self.offset_y = min(max(cy - s // 2, 0), max(0, max_y - s))
        self.visible = True


    def render(self, painter: QPainter, scene: Scene) -> None:
        if not self.visible:
            return
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


