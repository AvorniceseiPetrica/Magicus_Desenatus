from models.objects.scene import Scene
from business.application.commands import Command
from business.application.interfaces import GameInterface
from business.application.state_machine import StateMachine


class Coordinator(GameInterface):
    def __init__(self, state_machine: StateMachine):
        self._sm = state_machine

    def handle_input(self, command: Command) -> Scene:
        # place for cross-cutting logic: validation
        return self._sm.handle(command)

    def current_scene(self) -> Scene:
        return self._sm.scene
