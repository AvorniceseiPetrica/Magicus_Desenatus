from typing import Optional
from PyQt5.QtGui import QPixmap


class DecalCache:
    def __init__(self):
        self._cache: dict[str, Optional[QPixmap]] = {}

    def get(self, path: str) -> Optional[QPixmap]:
        if not path:
            return None
        if path not in self._cache:
            pix = QPixmap(path)
            self._cache[path] = None if pix.isNull() else pix
        return self._cache[path]
