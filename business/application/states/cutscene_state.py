from typing import Optional
from models.objects.cutscene import Cutscene
from business.application.commands import Command
from business.application.states.abstract_state import AbstractState, StateId


class CutsceneState(AbstractState):
    def __init__(self, cutscene: Cutscene, next_state: StateId = StateId.WORLD):
        self._cutscene = cutscene
        self._next = next_state

    @property
    def scene(self) -> Cutscene:
        return self._cutscene

    def handle(self, command: Command) -> Optional[StateId]:
        if command is Command.CANCEL:  # skip
            return self._finish()
        if command is Command.CONFIRM:
            self._cutscene.index += 1
            if self._cutscene.index >= len(self._cutscene.lines):
                return self._finish()
        return None

    def _finish(self) -> StateId:
        self._cutscene.index = 0  # replayable next time
        return self._next
