# from fastapi import APIRouter, HTTPException, Query
# from fastapi.responses import JSONResponse
# import requests
# from bs4 import BeautifulSoup
# import fitz  # PyMuPDF

# router = APIRouter()

# def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
#     text = ""
#     with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
#         for page in doc:
#             text += page.get_text()
#     return text.strip()

# def extract_text_from_html(url: str) -> str:
#     res = requests.get(url)
#     res.raise_for_status()
#     soup = BeautifulSoup(res.text, "html.parser")

#     # Remove scripts, styles, and hidden elements
#     for element in soup(["script", "style", "noscript"]):
#         element.decompose()

#     text = soup.get_text(separator=" ")
#     return " ".join(text.split()).strip()

# @router.get("/extract_text")
# async def extract_text(url: str = Query(..., description="URL of the resource to extract text from")):
#     if not url:
#         raise HTTPException(status_code=400, detail="No URL provided")

#     try:
#         # HEAD request to detect content type
#         head = requests.head(url, allow_redirects=True)
#         content_type = head.headers.get("Content-Type", "").lower()

#         if "pdf" in content_type or url.lower().endswith(".pdf"):
#             res = requests.get(url)
#             res.raise_for_status()
#             text = extract_text_from_pdf_bytes(res.content)
#         else:
#             text = extract_text_from_html(url)

#         return JSONResponse(content={"url": url, "text": text})

#     except requests.HTTPError as e:
#         raise HTTPException(status_code=502, detail=f"Failed to fetch URL: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")
