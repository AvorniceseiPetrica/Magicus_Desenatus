from models.objects.elements import Direction

_STEP = {(0, -1): Direction.UP, (0, 1): Direction.DOWN,
         (-1, 0): Direction.LEFT, (1, 0): Direction.RIGHT}

def path_to_directions(nodes) -> tuple[Direction, ...]:
    """Grid nodes (x, y) in drawing order -> one Direction per hop. Raises on diagonals/jumps."""
    out = []
    for (x0, y0), (x1, y1) in zip(nodes, nodes[1:]):
        step = _STEP.get((x1 - x0, y1 - y0))
        if step is None:
            raise ValueError(f"non-adjacent hop {(x0, y0)} -> {(x1, y1)}")
        out.append(step)
    return tuple(out)