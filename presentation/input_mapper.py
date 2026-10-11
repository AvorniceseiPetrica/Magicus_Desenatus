from typing import Optional
from PyQt5.QtCore import Qt
from business.application.commands import Command

_KEYMAP = {
    Qt.Key_Up: Command.UP, Qt.Key_Down: Command.DOWN,
    Qt.Key_Left: Command.LEFT, Qt.Key_Right: Command.RIGHT,
    Qt.Key_Return: Command.CONFIRM, Qt.Key_Escape: Command.CANCEL,
}


def to_command(key: int) -> Optional[Command]:
    return _KEYMAP.get(key)
