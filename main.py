import sys
from PySide6.QtWidgets import QApplication
from mainWindow import MainWindow

import os


if __name__ == "__main__":
    app = QApplication(sys.argv)
    os.environ["QT_IMAGEIO_MAXALLOC"] = str(512 * 1024 * 1024)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())