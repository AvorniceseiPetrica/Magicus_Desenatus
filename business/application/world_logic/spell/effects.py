from abc import ABC, abstractmethod
from models.objects.elements import AffinityType, Direction
from models.objects.actions import *
from models.objects.entity import Entity
from models.objects.world import World
from ..action_applier import ActionApplier


class ResolutionContext:
    """Simulation world + the actions emitted so far. Every emit is applied immediately,
    so later steps of the same spell see earlier consequences (knockback, deaths)."""

    def __init__(self, world: World, applier: ActionApplier):
        self.world, self.actions, self._applier = world, [], applier

    def emit(self, action: Action) -> None:
        self._applier.apply(self.world, action)
        self.actions.append(action)

    def damage(self, target: Entity, amount: int) -> None:
        amount = min(amount, target.hp)
        if amount > 0:
            self.emit(HpChanged(target.id, -amount))
            if target.hp <= 0:
                self.emit(EntityDied(target.id))

    def heal(self, target: Entity, amount: int) -> None:
        amount = min(amount, target.max_hp - target.hp)
        if amount > 0:
            self.emit(HpChanged(target.id, amount))

    def change_mana(self, target: Entity, delta: int) -> None:
        delta = max(-target.mana, min(delta, target.max_mana - target.mana))
        if delta:
            self.emit(ManaChanged(target.id, delta))

    def push(self, target: Entity, direction: Direction, tiles: int) -> None:
        dx, dy = direction.value
        for _ in range(tiles):
            dst = (target.x + dx, target.y + dy)
            if not self.world.is_free(*dst):
                break
            self.emit(EntityMoved(target.id, (target.x, target.y), dst))


class AffinityEffect(ABC):
    @abstractmethod
    def on_hit(self, ctx: ResolutionContext, caster: Entity, target: Entity, d: Direction) -> None: ...

    def on_aoe(self, ctx: ResolutionContext, caster: Entity, target: Entity) -> None: pass

    def on_self(self, ctx: ResolutionContext, caster: Entity) -> None: pass


class FireEffect(AffinityEffect):
    def on_hit(self, ctx, caster, target, d): ctx.damage(target, 3)

    def on_aoe(self, ctx, caster, target):    ctx.damage(target, 1)


class WaterEffect(AffinityEffect):
    def on_hit(self, ctx, caster, target, d):
        ctx.damage(target, 1);
        ctx.push(target, d, 2)

    def on_aoe(self, ctx, caster, target):    ctx.damage(target, 1)

    def on_self(self, ctx, caster):           ctx.change_mana(caster, 2)


class HolyEffect(AffinityEffect):
    def on_hit(self, ctx, caster, target, d): ctx.damage(target, 2)

    def on_self(self, ctx, caster):           ctx.heal(caster, 3)


class DarknessEffect(AffinityEffect):
    def on_hit(self, ctx, caster, target, d):
        ctx.damage(target, 1);
        ctx.change_mana(target, -2);
        ctx.change_mana(caster, 2)


def default_effects() -> dict[AffinityType, AffinityEffect]:
    return {AffinityType.FIRE: FireEffect(), AffinityType.WATER: WaterEffect(),
            AffinityType.HOLY: HolyEffect(), AffinityType.DARKNESS: DarknessEffect()}
