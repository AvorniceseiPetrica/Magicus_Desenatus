import sys
from PyQt5.QtWidgets import QApplication

import settings
from business.application.builder import build_coordinator
from presentation.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(build_coordinator())
    window.showFullScreen() if settings.FULLSCREEN else window.show()
    sys.exit(app.exec_())
