import os
from PyPDF2 import PdfReader

def load_pdf(path):
    reader = PdfReader(path)
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text or len(text.strip()) < 20:
            continue

        pages.append({
            "content": text,
            "page": i + 1,
            "document": os.path.basename(path)
        })

    return pages
