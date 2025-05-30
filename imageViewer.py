import PySide6
from PySide6.QtCore import Signal, QPointF, QRectF
from PySide6.QtGui import QPixmap, Qt, QMouseEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem

from SelectionRect import SelectionRectItem


class ImageViewer(QGraphicsView):
    mouseMoved = Signal(QPointF)  # Signal to send mouse position
    selectionChanged = Signal(QRectF)  # New signal for selection changes

    def __init__(self):
        super().__init__()

        # Create scene
        self.pixmap_item = None
        self.scene = QGraphicsScene(self)

        # Set scene to view
        self.setScene(self.scene)

        self.setMouseTracking(True)

        # Selection variables
        self.selection_rect = None
        self.selection_start = QPointF()
        self.selecting = False
        self.selection_mode = False

    def set_selection_mode(self, enabled):
        self.selection_mode = enabled

    def loadImage(self, image_path: str):
        # Remove existing image item if any
        if hasattr(self, 'pixmap_item') and self.pixmap_item is not None:
            self.scene.removeItem(self.pixmap_item)
            self.pixmap_item = None

        # Load and add new image
        pixmap = QPixmap(image_path)
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)

        # Fit the new image to view
        self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

    def clear_selection(self):
        if self.selection_rect:
            self.scene.removeItem(self.selection_rect)
            self.selection_rect = None
            self.selectionChanged.emit(QRectF())  # Emit empty rect

    def mouseMoveEvent(self, event: QMouseEvent):
        scene_pos = self.mapToScene(event.pos())
        self.mouseMoved.emit(scene_pos)  # Emit the scene coordinates

        if self.selection_mode and self.selecting and self.selection_rect:
            new_rect = QRectF(self.selection_start, scene_pos).normalized()
            self.selection_rect.setRect(new_rect)
            self.selectionChanged.emit(new_rect)  # Emit selection change
            return

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if self.selection_mode and event.button() == PySide6.QtCore.Qt.MouseButton.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            if self.scene.itemsBoundingRect().contains(scene_pos):
                self.selecting = True
                self.selection_start = scene_pos

                # Clear previous selection
                if self.selection_rect:
                    self.scene.removeItem(self.selection_rect)

                # Create new selection rectangle
                self.selection_rect = SelectionRectItem()
                self.selection_rect.setRect(QRectF(scene_pos, scene_pos))
                self.scene.addItem(self.selection_rect)
                return

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.selection_mode and event.button() == PySide6.QtCore.Qt.MouseButton.LeftButton and self.selecting:
            self.selecting = False
            # Optionally validate selection size here
            return

        super().mouseReleaseEvent(event)

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

    def get_selected_pixmap_with_coords(self):
        """Returns a tuple of (pixmap, top_left, bottom_right) or None if no selection"""
        if not self.selection_rect:
            return None

        # Get the selection rectangle in scene coordinates
        selection_rect = self.selection_rect.rect()

        # Convert to integer pixel coordinates in the original image
        top_left = selection_rect.topLeft().toPoint()
        bottom_right = selection_rect.bottomRight().toPoint()

        # Get the pixmap portion
        pixmap = self.pixmap_item.pixmap().copy(selection_rect.toRect())

        return (pixmap, top_left, bottom_right)
