from fastapi import APIRouter
from pydantic import BaseModel
from services.groq_client import query_groq

router = APIRouter()

class ChatRequest(BaseModel):
    user_input: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    content = await query_groq(req.user_input)
    return ChatResponse(response=content)
