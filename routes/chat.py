from fastapi import APIRouter
from pydantic import BaseModel
from services.groq_client import query_groq

router = APIRouter()

class ChatRequest(BaseModel):
    user_input: str

class ChatResponse(BaseModel):
    response: str
    
    
prompt = """You are the Explainer Agent. 
Your job is to help users understand complex words, phrases, or instructions in very simple and short language.

Rules:
- Keep answers short (1–3 sentences).
- Use everyday words, not technical jargon.
- If explaining a complex word, provide a simple definition and, if useful, a short example.
- If you don’t know, say: "I’m not sure about that."
"""

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    content = await query_groq(req.user_input)
    return ChatResponse(response=content)
