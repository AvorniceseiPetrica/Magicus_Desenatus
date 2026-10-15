from dataclasses import dataclass, field


@dataclass
class Grid:
    width: int = 5
    height: int = 5
    visited: list[tuple[int, int]] = field(default_factory=list) # tuplu de forma (x, y) ar fi in ordinea
    options: list[str] = field(default_factory=lambda: ["Confirm", "Reset"])

    # x 0 0       (0,0), (0, 1), (1, 1), (2, 2)
    # x x 0       luam fix ordinea pe care o avem...
    # 0 0 x
