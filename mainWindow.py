from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QAction, QShortcut, QKeySequence, QKeyEvent
from PySide6.QtWidgets import QMainWindow, QToolBar, QDialog, QLabel, QVBoxLayout

from Utils import FileUtils
from imageViewer import ImageViewer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_files = []
        self.CurrentIndex = -1
        self.setWindowTitle("Image Viewer")
        self.resize(1000, 800)
        self.viewer = ImageViewer()
        self.setCentralWidget(self.viewer)
        self.statusBar()  # Ensure status bar is created
        # Connect the signal
        self.viewer.mouseMoved.connect(self.update_status_bar)
        self.viewer.selectionChanged.connect(self.update_selection_status)

        # Setup toolbar with zoom controls
        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)

        convertPDFAction = QAction("convert pdf", self)
        convertPDFAction.triggered.connect(self.convert_pdf)
        toolbar.addAction(convertPDFAction)

        loadImagesAction = QAction("Load Images", self)
        loadImagesAction.triggered.connect(self.loadImgs)
        toolbar.addAction(loadImagesAction)

        zoom_in_action = QAction("Zoom In(I)", self)
        zoom_in_action.triggered.connect(self.viewer.zoom_in)
        toolbar.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out(O)", self)
        zoom_out_action.triggered.connect(self.viewer.zoom_out)
        toolbar.addAction(zoom_out_action)

        reset_zoom_action = QAction("Reset Zoom(R)", self)
        reset_zoom_action.triggered.connect(self.viewer.reset_zoom)
        toolbar.addAction(reset_zoom_action)

        # Selection actions
        select_action = QAction("Select (S)", self)
        select_action.setCheckable(True)
        select_action.triggered.connect(self.viewer.set_selection_mode)
        toolbar.addAction(select_action)

        clear_selection_action = QAction("Clear Selection", self)
        clear_selection_action.triggered.connect(self.viewer.clear_selection)
        toolbar.addAction(clear_selection_action)

        find_similarity_action = QAction("Find (F)", self)
        find_similarity_action.triggered.connect(self.find_similar_portions)
        toolbar.addAction(find_similarity_action)

        # ⌨️ Keyboard Shortcuts
        QShortcut(QKeySequence("i"), self, activated=self.viewer.zoom_in)
        QShortcut(QKeySequence("o"), self, activated=self.viewer.zoom_out)
        QShortcut(QKeySequence("r"), self, activated=self.viewer.reset_zoom)
        select_shortcut = QShortcut(QKeySequence("s"), self)
        select_shortcut.activated.connect(self.toggle_selection_mode)
        QShortcut(QKeySequence("Escape"), self, activated=self.viewer.clear_selection)
        QShortcut(QKeySequence("F"), self, activated=self.find_similar_portions)

    def loadImgs(self):
        folder_path = FileUtils.ask_for_folder(self, "Select Folder with Images")
        if folder_path:
            print("Selected folder:", folder_path)

            self.image_files = FileUtils.get_images_from_folder(folder_path)
            if not self.image_files:
                print("No Images :(")
                return

            print(f"Loading image {self.image_files[0]}")
            self.CurrentIndex = 0
            self.viewer.loadImage(self.image_files[self.CurrentIndex])

    def convert_pdf(self):
        FileUtils.select_and_convert_pdf_and_save(self, 200)

    def keyPressEvent(self, event: QKeyEvent):
        # Cmd on macOS is mapped to Ctrl by Qt for cross-platform compatibility
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_N:
                self.on_next()
            elif event.key() == Qt.Key.Key_P:
                self.on_previous()
        else:
            super().keyPressEvent(event)


    def update_status_bar(self, scene_pos: QPointF):
        x = int(scene_pos.x())
        y = int(scene_pos.y())
        # Clamp values within the image bounds
        if 0 <= x < self.viewer.scene.width() and 0 <= y < self.viewer.scene.height():
            self.statusBar().showMessage(f"Pixel: ({x}, {y})")
        else:
            self.statusBar().clearMessage()

    def update_selection_status(self, rect: QRectF):
        if rect.isNull():
            self.statusBar().showMessage("Selection cleared")
        else:
            pixel_rect = rect.toRect()
            self.statusBar().showMessage(
                f"Selection: ({pixel_rect.left()},{pixel_rect.top()}) to "
                f"({pixel_rect.right()},{pixel_rect.bottom()}) | "
                f"Size: {pixel_rect.width()}×{pixel_rect.height()}")

    def toggle_selection_mode(self):
        """Toggle selection mode and update action state"""
        self.viewer.set_selection_mode(not self.viewer.selection_mode)
        # Find and update the select action's checked state
        for action in self.findChildren(QAction):
            if action.text().startswith("Select"):
                action.setChecked(self.viewer.selection_mode)
                break

    def find_similar_portions(self):
        lPixmap, top_left, bottom_right = self.viewer.get_selected_pixmap_with_coords()
        if lPixmap is None:
            print("Pixmap is none")
            return

        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Selected Region Preview")

        # Coordinates label
        coords_label = QLabel(
            f"Top-left: ({top_left.x():.0f}, {top_left.y():.0f}) | "
            f"Bottom-right: ({bottom_right.x():.0f}, {bottom_right.y():.0f})"
        )
        coords_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Pixmap label
        image_label = QLabel()
        image_label.setPixmap(lPixmap)


        # Layout
        layout = QVBoxLayout()
        layout.addWidget(coords_label)
        layout.addWidget(image_label)

        dialog.setLayout(layout)
        dialog.exec()

    def on_next(self):
        self.CurrentIndex += 1
        if self.CurrentIndex == len(self.image_files):
           self.CurrentIndex -= 1
        self.viewer.loadImage(self.image_files[self.CurrentIndex])

    def on_previous(self):
        self.CurrentIndex -= 1
        if self.CurrentIndex == -1:
            self.CurrentIndex += 1
        self.viewer.loadImage(self.image_files[self.CurrentIndex])