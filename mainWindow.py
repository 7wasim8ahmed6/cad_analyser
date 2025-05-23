from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QMainWindow

from imageViewer import ImageViewer


class MainWindow(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.resize(1000, 800)
        self.viewer = ImageViewer(image_path)
        self.setCentralWidget(self.viewer)
        self.statusBar()  # Ensure status bar is created
        # Connect the signal
        self.viewer.mouseMoved.connect(self.update_status_bar)

    def update_status_bar(self, scene_pos: QPointF):
        x = int(scene_pos.x())
        y = int(scene_pos.y())
        # Clamp values within the image bounds
        if 0 <= x < self.viewer.scene.width() and 0 <= y < self.viewer.scene.height():
            self.statusBar().showMessage(f"Pixel: ({x}, {y})")
        else:
            self.statusBar().clearMessage()