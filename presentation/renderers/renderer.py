from abc import ABC, abstractmethod
from PyQt5.QtGui import QPainter
from models.objects.scene import Scene


class Renderer(ABC):
    @abstractmethod
    def render(self, painter: QPainter, scene: Scene) -> None:
        pass
