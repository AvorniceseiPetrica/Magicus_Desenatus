from dataclasses import dataclass, field
from models.objects.scene import Scene


@dataclass
class Menu(Scene):
    title: str = "Main Menu"
    options: list[str] = field(default_factory=lambda: ["Start", "Quit"])
    selected: int = 0
