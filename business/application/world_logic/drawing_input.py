from PyQt5.QtCore import QPoint

from models.objects.grid import Grid

# verifica cel mai apropiat nod
def nearest_node(grid: Grid, screen_pos: QPoint, cell_size: int, padding: int, threshold: int = 20) -> tuple[int,int] | None:
    for y in range(grid.height):
        for x in range(grid.width):
            nx = padding + x * cell_size
            ny = padding + y * cell_size
            dist = ((screen_pos.x() - nx)**2 + (screen_pos.y() - ny)**2) ** 0.5
            if dist < threshold:
                return (x, y)
    return None