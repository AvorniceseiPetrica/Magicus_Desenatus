from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QPushButton
from business.application.interfaces import GameInterface
from business.application.world_logic.drawing_input import nearest_node, verify_duplicated_nodes
from models.objects.grid import Grid
from models.objects.menu import Menu
from models.objects.world import World
from models.objects.cutscene import Cutscene
from presentation.input_mapper import to_command
from presentation.renderers.menu_renderer import MenuRenderer
from presentation.renderers.world_renderer import WorldRenderer, _TILE_SIZE
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
        self._grid_buttons()
        self._drawing = False
        self.resize(_TILE_SIZE * 25, _TILE_SIZE * 16)

        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self.update)
        self._anim_timer.start(16)

    def keyPressEvent(self, event):
        command = to_command(event.key())
        if command:
            self._game.handle_input(command)
            #self._update_ui()
            self.update()

    def _update_ui(self):
        scene = self._game.current_scene()
        if isinstance(scene, World):
            self._btn_confirm.setVisible(True)
            self._btn_reset.setVisible(True)
        else:
            self._btn_confirm.setVisible(False)
            self._btn_reset.setVisible(False)
        #Loc pentru alte butoane
        #TODO

    def paintEvent(self, _):
        scene = self._game.current_scene()
        painter = QPainter(self)
        self._renderers[type(scene)].render(painter, scene)

    def _get_grid(self) -> Grid | None:
        scene = self._game.current_scene()
        if isinstance(scene, World):
            return self._renderers[World].spell_grid
        return None

    #Event uri pentru grid ul de desenat
    def mousePressEvent(self, event):
        if not self._drawing:
            self._on_reset()
            self._drawing = True

    def mouseReleaseEvent(self, event):
        self._drawing = False

    def mouseMoveEvent(self, event):
        if not self._drawing:
            return
        spell_grid = self._get_grid()

        if spell_grid is None:
            return
        node = nearest_node(spell_grid, event.pos(), cell_size=60, padding=10)
        if node and verify_duplicated_nodes(spell_grid, node):
            spell_grid.visited.append(node)
            self.update()

    #Butoane pentru grid
    def _grid_buttons(self):
        self._btn_confirm = QPushButton("Confirm", self)
        self._btn_confirm.clicked.connect(self._on_confirm)

        self._btn_reset = QPushButton("Reset", self)
        self._btn_reset.clicked.connect(self._on_reset)

        self._btn_confirm.setVisible(False)
        self._btn_reset.setVisible(False)

        #pozitionarea butoanelor
        self._btn_confirm.setGeometry(360, 10, 100, 36)
        self._btn_reset.setGeometry(360, 56, 100, 36)

    def _on_confirm(self):
        grid = self._get_grid()
        if grid:
            print (grid.visited)

    def _on_reset(self):
        grid = self._get_grid()
        scene = self._game.current_scene()
        if grid and isinstance(scene, World):
            grid.visited.clear()
            self.update()