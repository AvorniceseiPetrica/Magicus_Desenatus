import copy
from typing import Callable, Optional

from models.objects.elements import Direction
from models.objects.frame import WorldFrame
from models.objects.world import World
from business.application.commands import Command, Input, SpellRequest
from business.application.playback.frame_builder import FrameBuilder
from business.application.playback.interpreter import ActionInterpreter
from business.application.world_logic.turn_processor import TurnProcessor
from business.application.states.abstract_state import AbstractState, StateId

_MOVES = {Command.UP: Direction.UP, Command.DOWN: Direction.DOWN,
          Command.LEFT: Direction.LEFT, Command.RIGHT: Direction.RIGHT}

class WorldState(AbstractState):
    def __init__(self, new_world: Callable[[], World], turns: TurnProcessor,
                 interpreter: ActionInterpreter, builder: FrameBuilder):
        self._new_world = new_world
        self._turns, self._interpreter, self._builder = turns, interpreter, builder
        self._world = new_world()
        self._frame = self._idle()

    @property
    def scene(self) -> WorldFrame:
        return self._frame

    def handle(self, command: Input) -> Optional[StateId]:
        if self._interpreter.is_playing:
            return None  # input locked while playing
        if command is Command.CANCEL:
            return StateId.MENU
        move = _MOVES.get(command)
        if move is None and not isinstance(command, SpellRequest):
            return None
        snapshot = copy.deepcopy(self._world)  # what the player sees right now
        actions = (self._turns.run_move(self._world, move) if move is not None
                   else self._turns.run_turn(self._world, command))  # logic is final immediately
        self._interpreter.start(snapshot, actions)
        if not actions:
            self._frame = self._idle()
        return None

    def update(self) -> Optional[StateId]:
        if not self._interpreter.is_playing:
            return None
        frame = self._interpreter.next_frame()
        if frame is not None:
            self._frame = frame
            return None
        if self._world.player is None:  # playback over and the hero died
            self._world = self._new_world()
            self._frame = self._idle()
            return StateId.MENU  # placeholder until a GAME_OVER state exists
        self._frame = self._idle()
        return None

    def _idle(self) -> WorldFrame:
        return self._builder.build(self._world, awaiting_input=True)
