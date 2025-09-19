from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests, tempfile, os
from pdfrw import PdfReader, PdfWriter
import json
from fastapi import APIRouter


router = APIRouter()
class PDFFillRequest(BaseModel):
    pdf_url: str
    form_data: dict  # JSON object of field-value pairs

@router.post("/fill-pdf/")
async def fill_pdf(request: PDFFillRequest):
    # Fetch the PDF (can be local or remote URL)
    if request.pdf_url.startswith("http://") or request.pdf_url.startswith("https://"):
        resp = requests.get(request.pdf_url)
        if resp.status_code != 200:
            return {"error": "Unable to fetch PDF"}
        pdf_bytes = resp.content
    else:
        # Local file path (handle static directory)
        local_path = request.pdf_url
        if local_path.startswith("/static/"):
            static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
            local_path = os.path.join(static_dir, os.path.relpath(local_path, "/static/"))
        with open(local_path, "rb") as f:
            pdf_bytes = f.read()

    # Save to temporary file
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_input.write(pdf_bytes)
    temp_input.close()

    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_output.close()

    # Read PDF and fill fields
    pdf_reader = PdfReader(temp_input.name)
    for page in pdf_reader.pages:
        if hasattr(page, "Annots"):
            for annot in page.Annots:
                if annot.Subtype == "/Widget" and annot.T:
                    key = annot.T[1:-1]  # remove parentheses
                    if key in request.form_data:
                        annot.V = f'{request.form_data[key]}'
                        annot.AP = None

    PdfWriter().write(temp_output.name, pdf_reader)
    os.remove(temp_input.name)

    return FileResponse(
        path=temp_output.name,
        filename="filled_pdf.pdf",
        media_type="application/pdf"
    )
