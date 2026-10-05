from abc import ABC, abstractmethod
from models.objects.entity import Entity
from models.objects.world import World
from business.application.world_logic.world_rules import move_or_attack


class EnemyAI(ABC):
    @abstractmethod
    def act(self, enemy: Entity, world: World) -> None:
        pass


class ChaseAI(EnemyAI):
    """Steps one tile toward the player along the larger axis."""

    def act(self, enemy: Entity, world: World) -> None:
        player = next((e for e in world.entities if e.is_player), None)
        if player is None:
            return
        dx, dy = player.x - enemy.x, player.y - enemy.y
        if abs(dx) >= abs(dy):
            step = (1 if dx > 0 else -1, 0)
        else:
            step = (0, 1 if dy > 0 else -1)
        move_or_attack(world, enemy, *step)
