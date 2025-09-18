from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.groq_client import query_groq
from services.user_database import user_db
from typing import Optional

router = APIRouter()

class ChatRequest(BaseModel):
    user_input: str
    user_id: Optional[str] = None  # Optional: Benutzer-ID für personalisierte Antworten

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # Benutzerdaten laden falls user_id vorhanden
    user_data = None
    if req.user_id:
        user = await user_db.get_user(req.user_id)
        if user:
            user_data = {
                "personal_info": {
                    "name": f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(),
                    "first_name": user.get('first_name', ''),
                    "last_name": user.get('last_name', ''),
                    "email": user.get('email', ''),
                    "phone": user.get('phone', ''),
                    "birth_date": user.get('birth_date', ''),
                    "birth_place": user.get('birth_place', ''),
                    "nationality": user.get('nationality', ''),
                    "marital_status": user.get('marital_status', ''),
                    "occupation": user.get('occupation', '')
                },
                "address": {
                    "street": user.get('street', ''),
                    "house_number": user.get('house_number', ''),
                    "postal_code": user.get('postal_code', ''),
                    "city": user.get('city', ''),
                    "country": user.get('country', '')
                },
                "financial": {
                    "bank_name": user.get('bank_name', ''),
                    "iban": user.get('iban', ''),
                    "bic": user.get('bic', ''),
                    "tax_id": user.get('tax_id', ''),
                    "social_security_number": user.get('social_security_number', '')
                }
            }
    
    # Erweiterte Eingabe mit Benutzerdaten für bessere KI-Antworten
    enhanced_input = req.user_input
    if user_data:
        enhanced_input = f"""
Benutzerdaten für personalisierte Hilfe:
Persönliche Daten: {user_data['personal_info']}
Adresse: {user_data['address']}
Finanzielle Daten: {user_data['financial']}

Benutzerfrage: {req.user_input}

Bitte verwende diese Informationen, um eine hilfreiche und personalisierte Antwort zu geben. Wenn der Benutzer nach Hilfe beim Ausfüllen von Formularen fragt, verwende die bereitgestellten Daten, um konkrete Vorschläge zu machen.
"""
    
    content = await query_groq(enhanced_input)
    return ChatResponse(response=content)
