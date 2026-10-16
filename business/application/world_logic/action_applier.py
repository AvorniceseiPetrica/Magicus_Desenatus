from models.objects.actions import *
from models.objects.world import World


class ActionApplier:
    def apply(self, world: World, action: Action) -> None:
        match action:
            case ManaChanged(entity_id=i, delta=d):
                e = world.get(i)
                e.mana = max(0, min(e.max_mana, e.mana + d))
            case HpChanged(entity_id=i, delta=d):
                e = world.get(i)
                e.hp = max(0, min(e.max_hp, e.hp + d))
            case EntityMoved(entity_id=i, dst=(x, y)):
                e = world.get(i)
                e.x, e.y = x, y
            case EntityDied(entity_id=i):
                world.entities = [e for e in world.entities if e.id != i]
            case _:
                pass  # purely visual actions

    def apply_all(self, world: World, actions: ActionList) -> None:
        for a in actions:
            self.apply(world, a)
