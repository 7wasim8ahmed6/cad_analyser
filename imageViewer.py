import PySide6
from PySide6.QtCore import Signal, QPointF
from PySide6.QtGui import QPixmap, Qt, QMouseEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem


class ImageViewer(QGraphicsView):
    mouseMoved = Signal(QPointF)  # Signal to send mouse position
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

        self.setMouseTracking(True)


        # Optional: fit the image to view size
        # self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

    def mouseMoveEvent(self, event: QMouseEvent):
        scene_pos = self.mapToScene(event.pos())
        self.mouseMoved.emit(scene_pos)  # Emit the scene coordinates
        super().mouseMoveEvent(event)

    def zoom_in(self):
        self.setTransformationAnchor(PySide6.QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.scale(1.25, 1.25)
        self.setTransformationAnchor(PySide6.QtWidgets.QGraphicsView.ViewportAnchor.AnchorViewCenter)

    def zoom_out(self):
        self.setTransformationAnchor(PySide6.QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.scale(0.8, 0.8)
        self.setTransformationAnchor(PySide6.QtWidgets.QGraphicsView.ViewportAnchor.AnchorViewCenter)

    def reset_zoom(self):
        self.resetTransform()
        self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)