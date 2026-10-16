# playback/interpreter.py
from itertools import chain
from typing import Iterator, Optional
from models.objects.actions import *
from models.objects.frame import Effect, EffectKind, WorldFrame
from models.objects.world import World
from business.application.world_logic.action_applier import ActionApplier
from .frame_builder import FrameBuilder

# frames per action (at 60 ticks/s, 8 frames is about 0.13 s); anything not listed gets 1
DURATION = {CastStarted: 6, CastFizzled: 14, ManaChanged: 8, HpChanged: 12,
            EntityMoved: 8, ProjectileMoved: 5, AoeReleased: 12, EntityDied: 10}

def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

class ActionInterpreter:
    """Turns an ActionList into a stream of frames, several frames per action.
    Works on its own snapshot of the world (taken BEFORE the spell was committed)
    and applies each action to it only after that action's animation finishes."""
    def __init__(self, applier: ActionApplier, builder: FrameBuilder):
        self._applier, self._builder = applier, builder
        self._view: Optional[World] = None
        self._frames: Iterator[WorldFrame] = iter(())
        self._playing = False

    @property
    def is_playing(self) -> bool:
        return self._playing

    def start(self, snapshot: World, actions: ActionList) -> None:
        self._view = snapshot
        self._frames = chain.from_iterable(self._animate(a) for a in actions)  # lazy
        self._playing = bool(actions)

    def next_frame(self) -> Optional[WorldFrame]:
        frame = next(self._frames, None)
        if frame is None:
            self._playing = False
        return frame

    def _animate(self, action: Action) -> Iterator[WorldFrame]:
        n = DURATION.get(type(action), 1)
        for i in range(1, n + 1):
            yield self._builder.build(self._view, **self._visuals(action, i / n))
        self._applier.apply(self._view, action)

    def _visuals(self, a: Action, t: float) -> dict:
        match a:
            case EntityMoved(entity_id=i, src=(sx, sy), dst=(dx, dy)):
                return {"positions": {i: (_lerp(sx, dx, t), _lerp(sy, dy, t))}}
            case ProjectileMoved(affinity=aff, src=(sx, sy), dst=(dx, dy)):
                return {"effects": [Effect(EffectKind.PROJECTILE, _lerp(sx, dx, t), _lerp(sy, dy, t), t, aff)]}
            case AoeReleased(affinity=aff, tiles=tiles):
                return {"effects": [Effect(EffectKind.BURST, x, y, t, aff) for x, y in tiles]}
            case EntityDied(entity_id=i):
                return {"alphas": {i: 1 - t}}
            case HpChanged(entity_id=i, delta=d) | ManaChanged(entity_id=i, delta=d):
                e = self._view.get(i)
                label = f"{d:+d}" + (" hp" if isinstance(a, HpChanged) else " mp")
                return {"effects": [Effect(EffectKind.TEXT, e.x, e.y - 0.6 * t, t, text=label)]}
            case CastStarted(caster_id=i, affinity=aff):
                e = self._view.get(i)
                return {"effects": [Effect(EffectKind.FLASH, e.x, e.y, t, aff)]}
            case CastFizzled(caster_id=i, reason=r):
                e = self._view.get(i)
                return {"effects": [Effect(EffectKind.TEXT, e.x, e.y - 0.6 * t, t, text=r)]}
            case _:
                return {}