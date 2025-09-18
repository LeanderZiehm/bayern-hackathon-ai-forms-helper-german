from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv


# Load GROQ_API_KEY from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Please set it in your .env file.")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

app = FastAPI(title="Groq Llama-3.3-70b API")

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:5500"] if serving HTML via Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Input schema
class ChatRequest(BaseModel):
    user_input: str

# Output schema
class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": req.user_input}
        ],
        "temperature": 0.7,
        "max_completion_tokens": 512
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(GROQ_API_URL, headers=headers, json=payload)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    data = r.json()
    content = data["choices"][0]["message"]["content"]

    return ChatResponse(response=content)
