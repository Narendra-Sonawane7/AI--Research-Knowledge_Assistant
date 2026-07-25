import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

# Change this path if Tesseract is installed elsewhere.
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_images(images):
    """
    Extract text from a list of PIL images.
    """
    text = ""

    for image in images:
        try:
            page_text = pytesseract.image_to_string(image)
            text += page_text + "\n"
        except Exception as e:
            print(f"OCR Error: {e}")

    return text


def extract_text_from_scanned_pdf(pdf_path):
    """
    Convert a scanned PDF into images and run OCR.
    """
    try:
        images = convert_from_path(
            pdf_path,
            poppler_path=r"C:\poppler\Library\bin"
        )
        return extract_text_from_images(images)

    except Exception as e:
        print(f"PDF OCR Error: {e}")
        return ""


def extract_text_from_image_file(image_path):
    """
    OCR for JPG/PNG files.
    """
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)

    except Exception as e:
        print(f"Image OCR Error: {e}")
        return ""


if __name__ == "__main__":

    sample = "sample.pdf"

    if os.path.exists(sample):
        result = extract_text_from_scanned_pdf(sample)

        print(result)