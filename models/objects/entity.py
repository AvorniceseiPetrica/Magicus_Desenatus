from dataclasses import dataclass


@dataclass
class Entity:
    name: str
    x: int
    y: int
    hp: int = 3
    decal: str = ""  # path/key of the sprite in models/decals/entities
    is_player: bool = False
