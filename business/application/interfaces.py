from abc import ABC, abstractmethod
from models.objects.scene import Scene
from business.application.commands import Command


class GameInterface(ABC):
    @abstractmethod
    def handle_input(self, command: Command) -> Scene:
        pass

    @abstractmethod
    def current_scene(self) -> Scene:
        pass
