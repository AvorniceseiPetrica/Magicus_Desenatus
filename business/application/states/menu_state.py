from typing import Optional
from models.objects.menu import Menu
from business.application.commands import Command
from business.application.states.abstract_state import AbstractState, StateId


class MenuState(AbstractState):
    def __init__(self, menu: Menu):
        self._menu = menu

    @property
    def scene(self) -> Menu:
        return self._menu

    def handle(self, command: Command) -> Optional[StateId]:
        n = len(self._menu.options)
        if command is Command.UP:
            self._menu.selected = (self._menu.selected - 1) % n
        elif command is Command.DOWN:
            self._menu.selected = (self._menu.selected + 1) % n
        elif command is Command.CONFIRM and self._menu.selected == 0:
            return StateId.WORLD
        return None
