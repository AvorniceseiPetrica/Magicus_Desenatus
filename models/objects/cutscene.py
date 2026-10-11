from dataclasses import dataclass, field
from models.objects.scene import Scene


@dataclass
class Cutscene(Scene):
    lines: list[str] = field(default_factory=list)
    index: int = 0
