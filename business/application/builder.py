import random

import settings
from business.application.playback.frame_builder import FrameBuilder
from business.application.world_logic.action_applier import ActionApplier
from business.application.world_logic.map_generator import generate_map
from business.application.world_logic.spell.effects import default_effects
from business.application.world_logic.spell.engine import SpellEngine
from business.application.world_logic.spell.rules import SpellRules
from business.application.world_logic.spell.spell_factory import SpellCastFactory
from business.application.world_logic.turn_processor import TurnProcessor
from models.objects.cutscene import Cutscene
from models.objects.entity import Entity, EntityState
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
from business.application.world_logic.map_reader import map_from_file

USE_RANDOM_MAP = False

def build_coordinator(seed: int | None = None) -> Coordinator:
    if USE_RANDOM_MAP:
        if seed is None:
            seed = random.randrange(2 ** 32)
        print("map seed:", seed)

        tiles = generate_map(*settings.RANDOM_MAP_SIZE, seed)

    else:
        tiles = map_from_file(settings.LEVELS_ROOT / settings.LEVEL)

    rules, applier, builder = SpellRules(), ActionApplier(), FrameBuilder()
    engine = SpellEngine(rules, default_effects(), applier)
    turns = TurnProcessor(SpellCastFactory(), engine, applier, ChaseAI(rules), rules)


    def new_world() -> World:
        return World(
            map=tiles,
            entities=[
                Entity("Hero", 1, 1, hp=5, is_player=True, sprites={
                    EntityState.IDLE: ("player/idle/idle_1.png",
                                       "player/idle/idle_2.png",
                                       "player/idle/idle_3.png",
                                       "player/idle/idle_4.png"
                                       ),
                    EntityState.MOVE: ("player/move/move_1.png",
                                       "player/move/move_2.png",
                                       "player/move/move_3.png",
                                       "player/move/move_4.png"
                                       )
                }),
                Entity("Goblin", 7, 6, sprites={
                    EntityState.IDLE: ("enemies/level1/goblin.png",),
                }),
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
