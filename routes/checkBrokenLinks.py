from fastapi import APIRouter
from pydantic import BaseModel
import re
import httpx
import asyncio  # <-- needed for gather

router = APIRouter()

URL_REGEX = r'https?://[^\s]+'

class TextRequest(BaseModel):
    text: str

async def is_link_broken(url: str) -> bool:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.head(url, follow_redirects=True)
            return response.status_code >= 400
    except Exception:
        return True

@router.post("/check-links")
async def check_links(request: TextRequest):
    text = request.text
    urls = re.findall(URL_REGEX, text)
    
    # Run all link checks concurrently using asyncio.gather
    results = await asyncio.gather(*[is_link_broken(url) for url in urls])
    
    for url, broken in zip(urls, results):
        if broken:
            text = text.replace(url, f"[BROKEN LINK {url} BROKEN LINK]")
    
    return {"processed_text": text}
