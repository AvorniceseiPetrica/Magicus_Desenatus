from models.objects.entity import Entity
from models.objects.world import World


def entity_at(world: World, x: int, y: int) -> Entity | None:
    return next((e for e in world.entities if e.x == x and e.y == y), None)


def in_bounds(world: World, x: int, y: int) -> bool:
    return 0 <= x < world.width and 0 <= y < world.height


def move_or_attack(world: World, actor: Entity, dx: int, dy: int) -> bool:
    """Returns True if the actor used its action (moved or attacked)."""
    x, y = actor.x + dx, actor.y + dy
    if not in_bounds(world, x, y):
        return False
    target = entity_at(world, x, y)
    if target is None:
        actor.x, actor.y = x, y
        return True
    if target.is_player != actor.is_player:  # only attack the opposing side
        target.hp -= 1
        if target.hp <= 0:
            world.entities.remove(target)
        return True
    return False
