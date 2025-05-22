from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem


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
        self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
