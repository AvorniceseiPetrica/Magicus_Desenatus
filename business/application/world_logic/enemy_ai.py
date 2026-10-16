from abc import ABC, abstractmethod
from models.objects.elements import Direction
from models.objects.entity import Entity
from models.objects.world import World
from business.application.commands import SpellKind, SpellRequest
from business.application.world_logic.spell.rules import SpellRules

class EnemyAI(ABC):
    @abstractmethod
    def choose_spell(self, enemy: Entity, world: World) -> SpellRequest: ...

class ChaseAI(EnemyAI):
    """Shoots if the player is in a straight line and in range, otherwise steps toward them."""
    def __init__(self, rules: SpellRules):
        self._range = rules.directional_step

    def choose_spell(self, enemy, world):
        player = world.player
        if player is None:
            return SpellRequest(enemy.affinity, SpellKind.SELF, ())
        dx, dy = player.x - enemy.x, player.y - enemy.y
        if (dx == 0 or dy == 0) and abs(dx) + abs(dy) <= self._range:
            return SpellRequest(enemy.affinity, SpellKind.DIRECTIONAL, (self._dir(dx, dy),))
        horizontal = abs(dx) >= abs(dy)
        step = self._dir(dx, 0) if horizontal else self._dir(0, dy)
        return SpellRequest(enemy.affinity, SpellKind.SELF, (step,))

    @staticmethod
    def _dir(dx: int, dy: int) -> Direction:
        if dx: return Direction.RIGHT if dx > 0 else Direction.LEFT
        return Direction.DOWN if dy > 0 else Direction.UP