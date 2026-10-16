# turn_processor.py
from models.objects.actions import ActionList, EntityDied, EntityMoved, ManaChanged
from models.objects.elements import Direction
from models.objects.entity import Entity
from models.objects.world import World
from .action_applier import ActionApplier
from business.application.commands import SpellRequest
from .enemy_ai import EnemyAI
from .spell.engine import SpellEngine
from .spell.rules import SpellRules
from business.application.world_logic.spell.spell_factory import SpellCastFactory

class TurnProcessor:
    """One full round: the player casts, then each living enemy casts, in order.
    Each cast is resolved against the world as left by the previous cast,
    and committed immediately. The result is one long ActionList."""
    def __init__(self, factory: SpellCastFactory, engine: SpellEngine,
                 applier: ActionApplier, ai: EnemyAI, rules: SpellRules):
        self._factory, self._engine, self._applier = factory, engine, applier
        self._ai, self._rules = ai, rules

    def run_turn(self, world: World, player_request: SpellRequest) -> ActionList:
        actions: ActionList = []
        if world.player:
            actions += self._cast(world, world.player, player_request)
        return actions + self._end_turn(world)

    def run_move(self, world: World, direction: Direction) -> ActionList:
        """Test movement with the arrow keys: one step, then the usual enemy phase."""
        player = world.player
        if player is None:
            return []
        x, y = player.x + direction.value[0], player.y + direction.value[1]
        if not (world.in_bounds(x, y) and world.map[y][x].props.walkable
                and world.entity_at(x, y) is None):
            return []  # blocked: no turn used
        actions: ActionList = [EntityMoved(player.id, (player.x, player.y), (x, y))]
        if world.map[y][x].props.deadly:
            actions.append(EntityDied(player.id))  # fell into a chasm
        self._applier.apply_all(world, actions)
        return actions + self._end_turn(world)

    def _end_turn(self, world: World) -> ActionList:
        actions: ActionList = []
        for enemy in world.enemies:
            if world.get(enemy.id) is None or world.player is None:
                continue  # died mid-round / player is dead
            actions += self._cast(world, enemy, self._ai.choose_spell(enemy, world))
        actions += self._regen(world)
        world.turn += 1
        return actions

    def _cast(self, world: World, caster: Entity, request: SpellRequest) -> ActionList:
        cast = self._factory.create(caster, request)
        actions = self._engine.resolve(cast, world)
        self._applier.apply_all(world, actions)
        return actions

    def _regen(self, world: World) -> ActionList:
        actions = [ManaChanged(e.id, min(self._rules.mana_regen, e.max_mana - e.mana))
                   for e in world.entities if e.mana < e.max_mana]
        self._applier.apply_all(world, actions)
        return actions