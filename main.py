from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap, Qt
import sys

class ImageViewer(QGraphicsView):
    def __init__(self, image_path):
        super().__init__()

        # Create scene
        self.scene = QGraphicsScene(self)

        # Load image into QPixmap
        pixmap = QPixmap(image_path)

        # Add QPixmap to scene
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)

        # Set scene to view
        self.setScene(self.scene)

        # Optional: fit the image to view size
        self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)  # mode=1 is Qt.KeepAspectRatio

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer("sample.png")
    viewer.setWindowTitle("QGraphicsView Image Viewer")
    viewer.resize(800, 600)
    viewer.show()
    sys.exit(app.exec())