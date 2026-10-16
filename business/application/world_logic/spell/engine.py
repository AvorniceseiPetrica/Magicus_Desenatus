import copy
from models.objects.actions import *
from models.objects.spell import PropagationType, SpellCast
from models.objects.world import World
from ..action_applier import ActionApplier
from .effects import AffinityEffect, ResolutionContext
from .rules import SpellRules

class SpellEngine:
    """Pure: never mutates the world it is given. Returns what WOULD happen."""
    def __init__(self, rules: SpellRules, effects: dict, applier: ActionApplier):
        self._rules, self._effects, self._applier = rules, effects, applier

    def resolve(self, cast: SpellCast, world: World) -> ActionList:
        prop = cast.propagation
        if not prop.directions:
            return []                                        # empty spell = pass
        ctx = ResolutionContext(copy.deepcopy(world), self._applier)
        caster = ctx.world.get(cast.caster.id)
        cost = self._rules.mana_cost(prop)
        if caster.mana < cost:
            ctx.emit(CastFizzled(caster.id, "Not enough mana"))
            return ctx.actions

        affinity = cast.affinity.type
        effect = self._effects[affinity]
        ctx.emit(CastStarted(caster.id, affinity))
        ctx.emit(ManaChanged(caster.id, -cost))
        if prop.type is PropagationType.SELF:
            self._resolve_self(ctx, cast, caster, effect)
        else:
            self._resolve_directional(ctx, cast, caster, effect)
        return ctx.actions

    def _resolve_self(self, ctx, cast, caster, effect: AffinityEffect) -> None:
        step = self._rules.step_length(cast.propagation)
        for d in cast.propagation.directions:
            dx, dy = d.value
            for _ in range(step):
                dst = (caster.x + dx, caster.y + dy)
                if not ctx.world.is_free(*dst):
                    break
                ctx.emit(EntityMoved(caster.id, (caster.x, caster.y), dst))
        effect.on_self(ctx, caster)

    def _resolve_directional(self, ctx, cast, caster, effect: AffinityEffect) -> None:
        step = self._rules.step_length(cast.propagation)
        affinity = cast.affinity.type
        pos = (caster.x, caster.y)
        for d in cast.propagation.directions:
            dx, dy = d.value
            for _ in range(step):                            # first tile = adjacent to start
                nxt = (pos[0] + dx, pos[1] + dy)
                if not ctx.world.flyable(*nxt):
                    break                                    # wall / map edge ends the arrow
                ctx.emit(ProjectileMoved(affinity, pos, nxt))
                pos = nxt
                target = ctx.world.entity_at(*nxt)
                if target and target.id != caster.id:
                    effect.on_hit(ctx, caster, target, d)
                    break                                    # arrow ends where it hits
        if cast.propagation.aoe_at_end:
            self._release_aoe(ctx, caster, effect, affinity, pos)

    def _release_aoe(self, ctx, caster, effect, affinity, center) -> None:
        r = self._rules.aoe_radius
        tiles = tuple((center[0] + dx, center[1] + dy)
                      for dy in range(-r, r + 1) for dx in range(-r, r + 1)
                      if ctx.world.flyable(center[0] + dx, center[1] + dy))
        ctx.emit(AoeReleased(affinity, center, tiles))
        victims = [e for t in tiles if (e := ctx.world.entity_at(*t)) and e.id != caster.id]
        for v in victims:
            effect.on_aoe(ctx, caster, v)