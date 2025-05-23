from PySide6.QtWidgets import QMainWindow

from imageViewer import ImageViewer


class MainWindow(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.resize(1000, 800)
        self.viewer = ImageViewer(image_path)
        self.setCentralWidget(self.viewer)