import fitz  # PyMuPDF

from app.utils.text_utils import chunk_text
from app.services.ocr_service import extract_text_from_scanned_pdf


def extract_pages_and_chunks(pdf_path: str):

    doc = fitz.open(pdf_path)

    pages_data = []
    all_chunks = []

    for page_num in range(len(doc)):

        page = doc[page_num]

        text = page.get_text().strip()

        # If no text found, use OCR
        if not text:

            print("=" * 50)
            print(f"OCR ACTIVATED FOR PAGE {page_num + 1}")
            print("=" * 50)

            text = extract_text_from_scanned_pdf(pdf_path).strip()

        # Skip empty pages
        if not text:
            continue

        pages_data.append(
            {
                "page": page_num + 1,
                "text": text
            }
        )

        chunks = chunk_text(text)

        for chunk in chunks:

            all_chunks.append(
                {
                    "page": page_num + 1,
                    "text": chunk
                }
            )

    print(f"Pages Extracted : {len(pages_data)}")
    print(f"Chunks Created  : {len(all_chunks)}")

    return len(doc), pages_data, all_chunks
