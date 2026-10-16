# presentation/spell_selector.py
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QButtonGroup, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from business.application.commands import SpellKind
from models.objects.elements import AffinityType

_KINDS = {SpellKind.SELF: "Self", SpellKind.DIRECTIONAL: "Directional",
          SpellKind.DIRECTIONAL_AOE: "Directional + AOE"}

class SpellSelector(QWidget):
    """Affinity and type sections. The path section is the grid you draw on."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.affinity = AffinityType.FIRE
        self.kind = SpellKind.DIRECTIONAL
        col = QVBoxLayout(self)
        col.setContentsMargins(0, 0, 0, 0)
        col.addLayout(self._row({a: a.value.title() for a in AffinityType}, "affinity"))
        col.addLayout(self._row(_KINDS, "kind"))

    def _row(self, options: dict, attr: str) -> QHBoxLayout:
        row, group = QHBoxLayout(), QButtonGroup(self)
        for key, text in options.items():
            b = QPushButton(text)
            b.setCheckable(True)
            b.setFocusPolicy(Qt.NoFocus)                  # keep Esc/F11 on the main window
            b.setChecked(getattr(self, attr) == key)
            b.clicked.connect(lambda _=False, k=key: setattr(self, attr, k))
            group.addButton(b)
            row.addWidget(b)
        return row