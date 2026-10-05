from models.objects.world import World
from business.application.world_logic.enemy_ai import EnemyAI


class TurnManager:
    def __init__(self, enemy_ai: EnemyAI):
        self._ai = enemy_ai

    def end_player_turn(self, world: World) -> None:
        for entity in list(world.entities):  # copy: entities may die mid-loop
            if not entity.is_player:
                self._ai.act(entity, world)
        world.turn += 1
