from PySide6.QtWidgets import QFileDialog, QMessageBox
from pdf2image import convert_from_path
from pathlib import Path

def select_and_convert_pdf_and_save(parent=None, dpi=300, fmt='png'):
    """
    Prompts the user to select a PDF file and a folder to save the converted images.

    Args:
        parent: The parent widget (usually self).
        dpi (int): Dots per inch for conversion quality.
        fmt (str): Image format to save (e.g., 'png', 'jpeg').

    Returns:
        List of saved file paths if successful, else None.
    """
    # Step 1: Select PDF file
    pdf_path, _ = QFileDialog.getOpenFileName(
        parent,
        "Select PDF File",
        "",
        "PDF Files (*.pdf)"
    )

    if not pdf_path:
        return None  # User cancelled

    # Step 2: Ask where to save the images
    output_dir = QFileDialog.getExistingDirectory(
        parent,
        "Select Folder to Save Images"
    )

    if not output_dir:
        return None  # User cancelled

    try:
        # Step 3: Convert to high-quality images
        images = convert_from_path(pdf_path, dpi=dpi, fmt=fmt)

        # Step 4: Save each page
        saved_paths = []
        for i, img in enumerate(images):
            output_path = Path(output_dir) / f"page_{i + 1}.{fmt}"
            img.save(output_path)
            saved_paths.append(str(output_path))

        return saved_paths

    except Exception as e:
        QMessageBox.critical(parent, "Conversion Error", f"Failed to convert PDF:\n{e}")
        return None

def ask_for_folder(parent=None, title="Select Folder"):
    folder = QFileDialog.getExistingDirectory(
        parent,
        title,
        "",  # Starting directory
        QFileDialog.Option.ShowDirsOnly
    )
    return folder if folder else None

def get_images_from_folder(folder_path):
    folder = Path(folder_path)
    return sorted([str(f) for f in folder.iterdir() if f.suffix.lower() in {'.png', '.jpg', '.jpeg'}])