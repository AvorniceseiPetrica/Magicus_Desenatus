from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget
from business.application.interfaces import GameInterface
from models.objects.menu import Menu
from models.objects.world import World
from models.objects.cutscene import Cutscene
from presentation.input_mapper import to_command
from presentation.renderers.menu_renderer import MenuRenderer
from presentation.renderers.world_renderer import WorldRenderer
from presentation.renderers.cutscene_renderer import CutsceneRenderer


class MainWindow(QWidget):
    def __init__(self, game: GameInterface):
        super().__init__()
        self._game = game
        self._renderers = {  # scene type -> renderer
            Menu: MenuRenderer(),
            World: WorldRenderer(),
            Cutscene: CutsceneRenderer(),
        }
        self.resize(800, 600)

    def keyPressEvent(self, event):
        command = to_command(event.key())
        if command:
            self._game.handle_input(command)
            self.update()

    def paintEvent(self, _):
        scene = self._game.current_scene()
        painter = QPainter(self)
        self._renderers[type(scene)].render(painter, scene)
