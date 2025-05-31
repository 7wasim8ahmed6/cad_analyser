import cv2
import numpy as np
from PySide6.QtWidgets import QFileDialog, QMessageBox
from pdf2image import convert_from_path
from pathlib import Path
from PySide6.QtGui import QImage

class FileUtils:

    @staticmethod
    def select_and_convert_pdf_and_save(parent=None, dpi=300, fmt='png'):
        """
        Prompts the user to select a PDF file and a folder to save the converted images.
        Returns a list of saved file paths or None.
        """
        pdf_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Select PDF File",
            "",
            "PDF Files (*.pdf)"
        )

        if not pdf_path:
            return None

        output_dir = QFileDialog.getExistingDirectory(
            parent,
            "Select Folder to Save Images"
        )

        if not output_dir:
            return None

        try:
            images = convert_from_path(pdf_path, dpi=dpi, fmt=fmt)
            saved_paths = []

            for i, img in enumerate(images):
                output_path = Path(output_dir) / f"page_{i + 1}.{fmt}"
                img.save(output_path)
                saved_paths.append(str(output_path))

            return saved_paths

        except Exception as e:
            QMessageBox.critical(parent, "Conversion Error", f"Failed to convert PDF:\n{e}")
            return None

    @staticmethod
    def ask_for_folder(parent=None, title="Select Folder"):
        folder = QFileDialog.getExistingDirectory(
            parent,
            title,
            "",  # Starting directory
            QFileDialog.Option.ShowDirsOnly
        )
        return folder if folder else None

    @staticmethod
    def get_images_from_folder(folder_path):
        folder = Path(folder_path)
        return sorted([str(f) for f in folder.iterdir() if f.suffix.lower() in {'.png', '.jpg', '.jpeg'}])

    @staticmethod
    def qpixmap_to_cv(pixmap):
        image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGB888)
        width, height = image.width(), image.height()
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        arr = np.array(ptr).reshape((height, width, 3))
        return arr  # OpenCV image in RGB

    @staticmethod
    def find_template_matches(full_pixmap, template_pixmap, threshold=0.8):
        full_img = FileUtils.qpixmap_to_cv(full_pixmap)
        template_img = FileUtils.qpixmap_to_cv(template_pixmap)

        # Convert to grayscale for better results (optional but recommended)
        full_gray = cv2.cvtColor(full_img, cv2.COLOR_RGB2GRAY)
        template_gray = cv2.cvtColor(template_img, cv2.COLOR_RGB2GRAY)

        result = cv2.matchTemplate(full_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)

        matches = []
        w, h = template_gray.shape[1], template_gray.shape[0]
        for pt in zip(*loc[::-1]):  # x, y
            matches.append((pt[0], pt[1], w, h))  # (x, y, width, height)
        return matches
