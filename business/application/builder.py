import random

from business.application.world_logic.map_generator import generate_map
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
from business.application.world_logic.map_reader import map_from_text

USE_RANDOM_MAP = False

_LEVEL = [
    "WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL",
    "WAL FL2 FD3 FL1 FD3 FL2 FD3 FL1 FD3 FL2 FD3 FL1 FD3 FL2 FD3 FL1 FD3 FL2 FD3 FL1 FD3 FL2 FD3 FL1 WAL",
    "WAL FD2 WAL WAL WAL WAL FL2 FD2 FL1 FD2 FL2 FD2 CHA CHA CHA FD2 FL1 FD2 FL2 FD2 WAL WAL WAL FD2 WAL",
    "WAL FL2 WAL FL1 FD1 FL2 FD1 FL1 FD1 FL2 FD1 FL1 FD1 CHA CHA CHA FD1 FL2 FD1 FL1 FD1 FL2 FD1 FL1 WAL",
    "WAL FD3 WAL FD3 FL1 WAL WAL WAL WAL FD3 FL2 FD3 FL1 CHA CHA CHA FL1 FD3 FL2 WAL WAL WAL WAL FD3 WAL",
    "WAL FL2 WAL FL1 FD2 WAL FD2 FL1 FD2 FL2 FD2 FL1 FD2 FL2 FD2 FL1 FD2 FL2 FD2 FL1 WAL FL2 FD2 FL1 WAL",
    "WAL FD1 FL2 FD1 FL1 WAL FL2 FD1 FL1 WAL WAL WAL WAL FD1 FL2 FD1 FL1 FD1 FL2 FD1 WAL FD1 FL2 FD1 WAL",
    "WAL FL2 WAL WAL WAL WAL FD3 FL1 FD3 WAL FD3 FL1 WAL FL2 FD3 FL1 CHA CHA FD3 FL1 WAL FL2 WAL WAL WAL",
    "WAL FD2 FL2 FD2 FL1 FD2 FL2 FD2 FL1 FD2 FL2 FD2 WAL FD2 FL2 FD2 CHA CHA FL2 FD2 FL1 FD2 FL2 FD2 WAL",
    "WAL FL2 WAL WAL WAL FL2 FD1 FL1 FD1 WAL WAL WAL WAL FL2 FD1 FL1 FD1 FL2 FD1 FL1 FD1 FL2 FD1 FL1 WAL",
    "WAL FD3 FL2 FD3 WAL FD3 FL2 FD3 FL1 FD3 FL2 FD3 CHA CHA CHA CHA FL1 FD3 WAL WAL WAL WAL FL2 FD3 WAL",
    "WAL FL2 WAL FL1 WAL FL2 WAL WAL WAL WAL FD2 FL1 CHA CHA CHA CHA FD2 FL2 WAL FL1 FD2 FL2 FD2 FL1 WAL",
    "WAL FD1 WAL FD1 FL1 FD1 FL2 FD1 FL1 FD1 WAL FD1 FL1 FD1 FL2 FD1 FL1 FD1 FL2 FD1 WAL FD1 WAL FD1 WAL",
    "WAL FL2 FD3 FL1 FD3 FL2 WAL WAL WAL WAL WAL FL1 FD3 FL2 FD3 WAL FD3 FL2 FD3 FL1 FD3 FL2 FD3 WAL WAL",
    "WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL WAL",
]

def build_coordinator(seed: int | None = None) -> Coordinator:
    if USE_RANDOM_MAP:
        if seed is None:
            seed = random.randrange(2 ** 32)
        print("map seed:", seed)

        tiles = generate_map(25, 15, seed)

    else:
        tiles = map_from_text(_LEVEL)

    def new_world() -> World:
        return World(
            map=tiles,
            entities=[
                Entity("Hero", 1, 1, hp=5, is_player=True, decal="player/default.png"),
                Entity("Goblin", 7, 6, decal="enemies/level1/goblin.png"),
            ],
        )

    states = {
        StateId.MENU: MenuState(Menu()),
        StateId.WORLD: WorldState(new_world, TurnManager(ChaseAI())),
        StateId.CUTSCENE: CutsceneState(
            Cutscene(lines=["Long ago...", "A magician set out.", "Press Enter to begin."])
        ),
    }
    return Coordinator(StateMachine(states, StateId.MENU))
