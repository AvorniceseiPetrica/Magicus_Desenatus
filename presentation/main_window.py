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

        self.resize(settings.WINDOWED_TILE_SIZE * settings.VIEW_COLUMNS,
                    settings.WINDOWED_TILE_SIZE * settings.VIEW_ROWS)

        self._update_ui()
        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._on_tick)
        self._anim_timer.start(settings.TICK_MS)

        self._place_hud_buttons()

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
        self._place_hud_buttons()
        view = self._renderers[WorldFrame].grid_view
        if view.visible:  # grila rămâne în fereastră după resize
            self._place_grid(view.offset_x + view.size // 2, view.offset_y + view.size // 2)

    def paintEvent(self, _):
        scene = self._game.current_scene()
        painter = QPainter(self)
        self._renderers[type(scene)].render(painter, scene)

    def _get_grid(self) -> Grid | None:
        scene = self._game.current_scene()
        if isinstance(scene, WorldFrame):
            return self._renderers[WorldFrame].spell_grid
        return None


    def _place_grid(self, cx: int, cy: int):
        """Centrează grila pe (cx, cy), fără să intre sub HUD-ul din dreapta."""
        lay = compute_layout(self.width(), self.height())
        self._renderers[WorldFrame].grid_view.place_at(cx, cy, lay.spell_panel_x, self.height())

    def _place_hud_buttons(self):
        lay = compute_layout(self.width(), self.height())
        self._btn_confirm.setGeometry(*lay.confirm_rect)
        self._btn_reset.setGeometry(*lay.reset_rect)
        for btn in (self._btn_confirm, self._btn_reset):
            font = btn.font()
            font.setPixelSize(lay.hud_font_px)
            btn.setFont(font)

    #Event uri pentru grid ul de desenat
    # click dreapta: grila apare / se mută la cursor
    # click stânga + tragere: desenează pe grilă (doar dacă grila e vizibilă)
    def mousePressEvent(self, event):
        if self._get_grid() is None:
            return
        view = self._renderers[WorldFrame].grid_view
        if event.button() == Qt.RightButton and not self._drawing:
            self._place_grid(event.pos().x(), event.pos().y())
            self.update()
        elif event.button() == Qt.LeftButton and view.visible and not self._drawing:
            self._on_reset()
            self._drawing = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drawing = False

    def mouseMoveEvent(self, event):
        if not self._drawing:
            return
        spell_grid = self._get_grid()

        if spell_grid is None:
            return

        view = self._renderers[WorldFrame].grid_view
        node = nearest_node(spell_grid, event.pos(), view.cell_size, view.padding,
                            view.offset_x, view.offset_y, threshold=view.cell_size // 2)
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
        print (grid.visited)
        grid.visited.clear()

    def _on_reset(self):
        grid = self._get_grid()
        if grid:
            grid.visited.clear()
            self.update()