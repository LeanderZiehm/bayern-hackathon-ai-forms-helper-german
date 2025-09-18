from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os

router = APIRouter()

UPLOAD_DIR = "static/uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    url = f"/static/uploaded/{file.filename}"
    return {"url": url}

@router.get("/uploaded")
async def get_uploaded_files():
    files = [
        f"/static/uploaded/{fname}"
        for fname in os.listdir(UPLOAD_DIR)
        if fname.endswith(".pdf")
    ]
    return JSONResponse(content={"files": files})