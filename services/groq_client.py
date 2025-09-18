import os
import httpx
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Please set it in your .env file.")


def get_system_message_object(user_system_message_text):
    return  [{"role": "system", "content": user_system_message_text}]
    
    

async def query_groq(user_input: str, system_prompt:str = "") -> str:
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    messages = [{"role": "user", "content": user_input}]
    
    if system_prompt != "":
        system_message_object = get_system_message_object(system_prompt)
        messages.insert(0,system_message_object)

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.7,
        "max_completion_tokens": 512
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(GROQ_API_URL, headers=headers, json=payload)

    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]
