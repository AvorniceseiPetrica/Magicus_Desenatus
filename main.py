import sys
from PyQt5.QtWidgets import QApplication, QWidget


def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle('Magus Desenatus')
    window.setGeometry(100, 100, 400, 200)

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()