import os
import httpx
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Please set it in your .env file.")

async def query_groq(user_input: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7,
        "max_completion_tokens": 512
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(GROQ_API_URL, headers=headers, json=payload)

    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]
