from dataclasses import dataclass


@dataclass
class Entity:
    name: str
    x: int
    y: int
    hp: int = 3
    decal: tuple[str, ...] = ()
    is_player: bool = False
