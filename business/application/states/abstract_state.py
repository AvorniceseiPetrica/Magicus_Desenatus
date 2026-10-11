from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional
from models.objects.scene import Scene
from business.application.commands import Command


class StateId(Enum):
    MENU = auto()
    WORLD = auto()
    CUTSCENE = auto()


class AbstractState(ABC):
    @property
    @abstractmethod
    def scene(self) -> Scene:
        pass

    @abstractmethod
    def handle(self, command: Command) -> Optional[StateId]:
        """Return a StateId to request a transition, or None to stay."""
        pass
