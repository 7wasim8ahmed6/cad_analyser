from PySide6.QtCore import QPointF
from PySide6.QtGui import QAction, QShortcut, QKeySequence
from PySide6.QtWidgets import QMainWindow, QToolBar

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

        # Setup toolbar with zoom controls
        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(self.viewer.zoom_in)
        toolbar.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.triggered.connect(self.viewer.zoom_out)
        toolbar.addAction(zoom_out_action)

        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.triggered.connect(self.viewer.reset_zoom)
        toolbar.addAction(reset_zoom_action)

        # ⌨️ Keyboard Shortcuts
        QShortcut(QKeySequence("i"), self, activated=self.viewer.zoom_in)
        QShortcut(QKeySequence("o"), self, activated=self.viewer.zoom_out)
        QShortcut(QKeySequence("r"), self, activated=self.viewer.reset_zoom)

    def update_status_bar(self, scene_pos: QPointF):
        x = int(scene_pos.x())
        y = int(scene_pos.y())
        # Clamp values within the image bounds
        if 0 <= x < self.viewer.scene.width() and 0 <= y < self.viewer.scene.height():
            self.statusBar().showMessage(f"Pixel: ({x}, {y})")
        else:
            self.statusBar().clearMessage()