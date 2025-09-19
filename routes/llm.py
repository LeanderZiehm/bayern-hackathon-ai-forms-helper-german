from fastapi import APIRouter
from pydantic import BaseModel
from services.groq_client import query_groq

router = APIRouter()

class LLMRequest(BaseModel):
    user_input: str
    system_prompt:str

class LLMResponse(BaseModel):
    response: str

@router.post("/llm", response_model=LLMResponse)
async def llm(req: LLMRequest):
    content = await query_groq(req.user_input,req.system_prompt)
    return LLMResponse(response=content)
