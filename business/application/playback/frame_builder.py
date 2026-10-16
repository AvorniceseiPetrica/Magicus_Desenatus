from models.objects.frame import Effect, EntityView, WorldFrame
from models.objects.world import World

class FrameBuilder:
    def build(self, world: World, *, positions=None, alphas=None,
              effects=(), awaiting_input=False) -> WorldFrame:
        positions, alphas = positions or {}, alphas or {}
        views = [EntityView(e.id, e.name, *positions.get(e.id, (e.x, e.y)),
                            e.hp, e.max_hp, e.mana, e.max_mana,
                            e.sprites, e.state, e.state_seq, e.is_player,
                            alphas.get(e.id, 1.0))
                 for e in world.entities]
        return WorldFrame(world.map, views, list(effects), world.turn, awaiting_input)