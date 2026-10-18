from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QPushButton

import settings
from business.application.commands import SpellRequest
from business.application.interfaces import GameInterface
from business.application.world_logic.drawing_input import nearest_node, verify_duplicated_nodes
from business.application.world_logic.path_comverter import path_to_directions
from models.objects.grid import Grid
from models.objects.menu import Menu
from models.objects.frame import WorldFrame
from models.objects.cutscene import Cutscene
from presentation.input_mapper import to_command
from presentation.layout import compute_layout
from presentation.renderers.menu_renderer import MenuRenderer
from presentation.renderers.world_renderer import WorldRenderer
from presentation.renderers.cutscene_renderer import CutsceneRenderer
from presentation.spell_selector import SpellSelector


class MainWindow(QWidget):
    def __init__(self, game: GameInterface):
        super().__init__()
        self._game = game
        self._renderers = {  # scene type -> renderer
            Menu: MenuRenderer(),
            WorldFrame: WorldRenderer(),
            Cutscene: CutsceneRenderer(),
        }
        self._selector = SpellSelector(self)
        self._selector.setGeometry(10, 10, 340, 80)
        self._grid_buttons()
        self._drawing = False

        default_h = settings.WINDOWED_TILE_SIZE * settings.VIEW_ROWS
        self.resize(settings.WINDOWED_TILE_SIZE * settings.VIEW_COLUMNS,
                    int(default_h / (1 - settings.HUD_RATIO)))

        self._update_ui()
        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._on_tick)
        self._anim_timer.start(settings.TICK_MS)

        self._grid_origin_x = settings.SPELL_PADDING
        self._grid_origin_y = 0
        self._recalc_grid_origin()

    def _on_tick(self):
        self._game.tick()  # asks WorldState for the next frame
        self._update_ui()
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            self.showNormal() if self.isFullScreen() else self.showFullScreen()
            return

        command = to_command(event.key())
        if command:
            self._game.handle_input(command)
            #self._update_ui()
            self.update()

    def _update_ui(self):
        scene = self._game.current_scene()
        if isinstance(scene, WorldFrame):
            self._btn_confirm.setVisible(True)
            self._btn_reset.setVisible(True)
        else:
            self._btn_confirm.setVisible(False)
            self._btn_reset.setVisible(False)
        #Loc pentru alte butoane
        #TODO

    # apelat de fiecare data cand se face resize la window
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._recalc_grid_origin()

    def paintEvent(self, _):
        scene = self._game.current_scene()
        painter = QPainter(self)
        self._renderers[type(scene)].render(painter, scene)

    def _get_grid(self) -> Grid | None:
        scene = self._game.current_scene()
        if isinstance(scene, WorldFrame):
            return self._renderers[WorldFrame].spell_grid
        return None


    def _recalc_grid_origin(self):
        from presentation.layout import compute_layout
        lay = compute_layout(self.width(), self.height())
        grid_pixel_size = settings.SPELL_PADDING + 4 * lay.spell_cell_size + settings.SPELL_PADDING
        self._grid_origin_x = settings.SPELL_PADDING
        self._grid_origin_y = lay.hud_y + (lay.hud_height - grid_pixel_size) // 2
        self._grid_cell_size = lay.spell_cell_size

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

        node = nearest_node(spell_grid, event.pos(), self._grid_cell_size, settings.SPELL_PADDING, self._grid_origin_x, self._grid_origin_y, threshold=self._grid_cell_size // 2)
        if node and verify_duplicated_nodes(spell_grid, node):
            spell_grid.visited.append(node)
            self.update()

    # TODO
    # TODO
    # TODO::::: THIS SHIT IS FUKED BEYOND REPAIR
    # TODO
    # TODO
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

        self._btn_confirm.setFocusPolicy(Qt.NoFocus)
        self._btn_reset.setFocusPolicy(Qt.NoFocus)

    def _on_confirm(self):
        grid = self._get_grid()
        if grid is None:
            return
        try:
            directions = path_to_directions(grid.visited)
        except ValueError:                         # diagonal or skipped node
            self._on_reset()
            return
        self._game.handle_input(
            SpellRequest(self._selector.affinity, self._selector.kind, directions))
        grid.visited.clear()

    def _on_reset(self):
        grid = self._get_grid()
        if grid:
            grid.visited.clear()
            self.update()