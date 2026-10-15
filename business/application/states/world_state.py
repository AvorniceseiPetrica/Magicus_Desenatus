from typing import Optional, Callable
from models.objects.world import World
from business.application.commands import Command
from business.application.world_logic.turn_manager import TurnManager
from business.application.world_logic.world_rules import move_or_attack
from business.application.states.abstract_state import AbstractState, StateId

_DIRECTIONS = {
    Command.UP: (0, -1), Command.DOWN: (0, 1),
    Command.LEFT: (-1, 0), Command.RIGHT: (1, 0),
}


class WorldState(AbstractState):
    def __init__(self, new_world: Callable[[], World], turn_manager: TurnManager):
        self._new_world = new_world
        self._world = new_world()
        self._turns = turn_manager

    @property
    def scene(self) -> World:
        return self._world

    def handle(self, command: Command) -> Optional[StateId]:
        if command is Command.CANCEL:
            return StateId.MENU
        direction = _DIRECTIONS.get(command)
        if direction is None:
            return None
        player = next((e for e in self._world.entities if e.is_player), None)
        if player and move_or_attack(self._world, player, *direction):
            self._turns.end_player_turn(self._world)
            if not any(e.is_player for e in self._world.entities):  # player died
                self._world = self._new_world()
                return StateId.MENU
        return None
