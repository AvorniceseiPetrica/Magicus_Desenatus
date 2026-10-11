from models.objects.scene import Scene
from business.application.commands import Command
from business.application.states.abstract_state import AbstractState, StateId


class StateMachine:
    def __init__(self, states: dict[StateId, AbstractState], initial: StateId):
        self._states = states
        self._current = states[initial]

    def handle(self, command: Command) -> Scene:
        next_id = self._current.handle(command)
        if next_id is not None:
            self._current = self._states[next_id]
        return self._current.scene

    @property
    def scene(self) -> Scene:
        return self._current.scene
