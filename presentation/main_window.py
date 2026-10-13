from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget
from business.application.interfaces import GameInterface
from business.application.world_logic.drawing_input import nearest_node
from models.objects.grid import Grid
from models.objects.menu import Menu
from models.objects.world import World
from models.objects.cutscene import Cutscene
from presentation.input_mapper import to_command
from presentation.renderers.grid_renderer import GridRenderer
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
        self._drawing = False

    def keyPressEvent(self, event):
        command = to_command(event.key())
        if command:
            self._game.handle_input(command)
            self.update()

    def paintEvent(self, _):
        scene = self._game.current_scene()
        painter = QPainter(self)
        self._renderers[type(scene)].render(painter, scene)


    #Event uri pentru grid ul de desenat
    def mousePressEvent(self, event):
        self._drawing = True

    def mouseReleaseEvent(self, event):
        self._drawing = False

    def _get_grid(self) -> Grid | None:
        scene = self._game.current_scene()
        if isinstance(scene, World):
            return self._renderers[World].spell_grid
        return None

    def mouseMoveEvent(self, event):
        if not self._drawing:
            return
        spell_grid = self._get_grid()

        if spell_grid is None:
            return
        node = nearest_node(spell_grid, event.pos(), cell_size=60, padding=10)
        if node:
            spell_grid.visited.append(node)
            self.update()



