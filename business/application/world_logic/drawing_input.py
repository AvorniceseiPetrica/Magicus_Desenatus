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

def verify_duplicated_nodes(grid: Grid, node: tuple[int, int]) -> bool:
    if len(grid.visited) == 0:
        return True

    last_node = grid.visited[-1]
    if last_node == node:
        return False

    for i in range (len(grid.visited) - 1):
        node1 = grid.visited[i]
        node2 = grid.visited[i + 1]

        print ("Verificam legatura: ", node1, " si: ", node2, " sa nu fie egal cu ", last_node, " si: ", node)

        #verificam daca exista deja legatura, daca exista returnam false
        if (node1 == last_node) and (node2 == node) or (node1 == node) and (node2 == last_node):
            return False

    return True