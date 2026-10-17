import json
from dataclasses import dataclass, field
from pathlib import Path

import settings
from models.objects.scene import Scene
@dataclass
class CutsceneObject:
    delay: int = 0
    position: tuple[float, float] = (0, 0)

@dataclass
class CutsceneImage(CutsceneObject):
    path: str = ""
    width: float = 0

@dataclass
class CutsceneTextBubble(CutsceneObject):
    text: str = ""
    max_width: float = 0

@dataclass
class CutsceneClearScreen(CutsceneObject):
    pass

@dataclass
class Cutscene(Scene):
    cutscene_objects: list[CutsceneObject] = field(default_factory=list)
    index: int = 0
    cutscene_dir: str = settings.CUTSCENE_ROOT
    time_last_shown: int = 0


_CUTSCENE_OBJECTS = {"Image": CutsceneImage, "Text": CutsceneTextBubble, "Clear": CutsceneClearScreen}
def loadCutscene(scene: str) -> Cutscene:
    cutscene_data = json.loads(Path(settings.CUTSCENE_ROOT / scene / "scene.json").read_text())
    elements = []
    for raw in cutscene_data["elements"]:
        raw = dict(raw)
        cls = _CUTSCENE_OBJECTS[raw.pop("type")]
        elements.append(cls(**raw))
    return Cutscene(cutscene_objects=elements, cutscene_dir= Path(settings.CUTSCENE_ROOT / scene))