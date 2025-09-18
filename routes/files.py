from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os

router = APIRouter()

PDF_DIR = "static/pdfs"

@router.get("/pdfs")
async def list_pdfs():
    pdf_files = []
    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            pdf_files.append({
                "name": filename,
                "url": f"/static/pdfs/{filename}"
            })
    return JSONResponse(content=pdf_files)
