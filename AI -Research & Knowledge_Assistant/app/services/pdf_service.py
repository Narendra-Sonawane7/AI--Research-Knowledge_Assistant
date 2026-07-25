import fitz  # PyMuPDF
from app.utils.text_utils import chunk_text
from app.services.ocr_service import (
    extract_text_from_scanned_pdf
)





def extract_pages_and_chunks(pdf_path: str):
    doc = fitz.open(pdf_path)
    pages_data = []
    all_chunks = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()

    if not text.strip():
        print("Using OCR...")
        print("=" * 50)
        print("OCR ACTIVATED")
        print("=" * 50)

        text = extract_text_from_scanned_pdf(pdf_path)

        print(text)

        pages_data.append({"page": page_num + 1, "text": text})
        for chunk in chunk_text(text):
            all_chunks.append({"page": page_num + 1, "text": chunk})

    return len(doc), pages_data, all_chunks
