from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services.pdf_reader import extract_text_from_pdf
from services.pdf_reader import get_pdf_title
import os

router = APIRouter()

PDF_DIR = "static/pdfs"

@router.get("/pdfs")
async def list_pdfs_with_titles():
    pdf_files = []
    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            try:
                title = get_pdf_title(filename)
            except Exception:
                title = filename  # fallback if error occurs

            pdf_files.append({
                "file_name": filename,
                "title": title,
                "url": f"/static/pdfs/{filename}"
            })
    return JSONResponse(content=pdf_files)

@router.get("/pdfs/{pdf_name}/text")
async def get_pdf_text(pdf_name: str):
    try:
        text = extract_text_from_pdf(pdf_name)
        return {"name": pdf_name, "text": text}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"PDF '{pdf_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
