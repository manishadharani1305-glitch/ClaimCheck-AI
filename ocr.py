import pytesseract
from PIL import Image
import shutil


def extract_text_from_image(image):
    tesseract_path = shutil.which("tesseract")

    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    text = pytesseract.image_to_string(image)

    return text