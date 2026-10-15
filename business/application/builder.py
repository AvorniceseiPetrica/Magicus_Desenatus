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
    "################",
    "#..............#",
    "#.####....####.#",
    "#.#....~~....#.#",
    "#.#....~~....#.#",
    "#......##......#",
    "#.#..........#.#",
    "#.#..........#.#",
    "#.####....####.#",
    "#..............#",
    "################",
]

def build_coordinator(seed: int | None = None) -> Coordinator:
    if USE_RANDOM_MAP:
        if seed is None:
            seed = random.randrange(2 ** 32)
        print("map seed:", seed)

        tiles = generate_map(25, 15, seed)

    else:
        tiles = map_from_text(_LEVEL)

    world = World(
        map=tiles,
        entities=[
            Entity("Hero", 1, 1, hp=5, is_player=True),
            Entity("Goblin", 7, 6),
        ],
    )

    states = {
        StateId.MENU: MenuState(Menu()),
        StateId.WORLD: WorldState(world, TurnManager(ChaseAI())),
        StateId.CUTSCENE: CutsceneState(
            Cutscene(lines=["Long ago...", "A magician set out.", "Press Enter to begin."])
        ),
    }
    return Coordinator(StateMachine(states, StateId.MENU))
