import fitz  # PyMuPDF
import os

PDF_DIR = "static/pdfs"

def extract_text_from_pdf(filename: str) -> str:
    file_path = os.path.join(PDF_DIR, filename)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"PDF '{filename}' not found.")

    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def get_pdf_title(filename: str) -> str:
    file_path = os.path.join(PDF_DIR, filename)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"PDF '{filename}' not found.")
    
    doc = fitz.open(file_path)
    metadata = doc.metadata  # returns a dict
    doc.close()
    
    title = metadata.get("title")  # may be None if not set
    if not title:
        title = filename  # fallback to file name
    return title