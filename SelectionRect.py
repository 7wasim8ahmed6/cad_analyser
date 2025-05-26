from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtCore import Qt


class SelectionRectItem(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Blue dashed line border
        pen = QPen(Qt.GlobalColor.blue, 2, Qt.PenStyle.DashLine)
        self.setPen(pen)

        # Semi-transparent blue fill
        brush = QBrush(QColor(0, 0, 255, 50))
        self.setBrush(brush)