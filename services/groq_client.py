import os
import httpx
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Please set it in your .env file.")

import httpx
async def query_groq(user_input: str, system_prompt: str = "") -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    messages = [{"role": "user", "content": user_input}]
    if system_prompt.strip():
        messages.insert(0, {"role": "system", "content": system_prompt})

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.7,
        "max_completion_tokens": 2048
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        # Always return a string, indicating an error
        return f"Error occurred: {str(e)}"
