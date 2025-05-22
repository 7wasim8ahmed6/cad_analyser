import sys
from PySide6.QtWidgets import QApplication
from imageViewer import ImageViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer("sample.png")
    viewer.setWindowTitle("QGraphicsView Image Viewer")
    viewer.resize(800, 600)
    viewer.show()
    sys.exit(app.exec())