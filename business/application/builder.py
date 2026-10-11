from models.objects.cutscene import Cutscene
from models.objects.entity import Entity
from models.objects.menu import Menu
from models.objects.world import World
from business.application.coordinator import Coordinator
from business.application.world_logic.enemy_ai import ChaseAI
from business.application.state_machine import StateMachine
from business.application.states.cutscene_state import CutsceneState
from business.application.states.abstract_state import StateId
from business.application.states.menu_state import MenuState
from business.application.states.world_state import WorldState
from business.application.world_logic.turn_manager import TurnManager


def build_coordinator() -> Coordinator:
    world = World(entities=[
        Entity("Hero", 1, 1, hp=5, is_player=True),
        Entity("Goblin", 7, 6),
    ])
    states = {
        StateId.MENU: MenuState(Menu()),
        StateId.WORLD: WorldState(world, TurnManager(ChaseAI())),
        StateId.CUTSCENE: CutsceneState(
            Cutscene(lines=["Long ago...", "A magician set out.", "Press Enter to begin."])
        ),
    }
    return Coordinator(StateMachine(states, StateId.MENU))
