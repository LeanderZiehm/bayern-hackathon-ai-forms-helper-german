from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from services.user_database import user_db
import re

router = APIRouter()

class UserRegistration(BaseModel):
    # Persönliche Daten
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    
    # Adressdaten
    street: Optional[str] = None
    house_number: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    country: str = "Deutschland"
    
    # Weitere wichtige Daten für Formulare
    birth_date: Optional[str] = None
    birth_place: Optional[str] = None
    nationality: str = "Deutsch"
    marital_status: Optional[str] = None
    occupation: Optional[str] = None
    
    # Bankdaten (optional)
    bank_name: Optional[str] = None
    iban: Optional[str] = None
    bic: Optional[str] = None
    
    # Steuerdaten
    tax_id: Optional[str] = None
    social_security_number: Optional[str] = None

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    birth_date: Optional[str] = None
    birth_place: Optional[str] = None
    nationality: Optional[str] = None
    marital_status: Optional[str] = None
    occupation: Optional[str] = None
    bank_name: Optional[str] = None
    iban: Optional[str] = None
    bic: Optional[str] = None
    tax_id: Optional[str] = None
    social_security_number: Optional[str] = None

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@router.post("/register")
async def register_user(user_data: UserRegistration):
    # Validierung
    if not validate_email(user_data.email):
        raise HTTPException(status_code=400, detail="Ungültige E-Mail-Adresse")
    
    # Prüfen ob E-Mail bereits existiert
    existing_user = await user_db.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="E-Mail-Adresse bereits registriert")
    
    # Benutzer erstellen
    try:
        user_id = await user_db.create_user(user_data.dict())
        return {
            "message": "Benutzer erfolgreich registriert",
            "user_id": user_id,
            "email": user_data.email
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}")
async def get_user(user_id: str):
    user = await user_db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    
    # Sensible Daten entfernen für die Antwort
    safe_user = user.copy()
    safe_user.pop('created_at', None)
    safe_user.pop('updated_at', None)
    
    return safe_user

@router.put("/user/{user_id}")
async def update_user(user_id: str, user_data: UserUpdate):
    user = await user_db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    
    # Nur vorhandene Felder aktualisieren
    update_data = {k: v for k, v in user_data.dict().items() if v is not None}
    
    if 'email' in update_data and not validate_email(update_data['email']):
        raise HTTPException(status_code=400, detail="Ungültige E-Mail-Adresse")
    
    success = await user_db.update_user(user_id, update_data)
    if not success:
        raise HTTPException(status_code=500, detail="Fehler beim Aktualisieren des Benutzers")
    
    return {"message": "Benutzer erfolgreich aktualisiert"}

@router.get("/user/{user_id}/form-data")
async def get_user_form_data(user_id: str):
    """Gibt die Benutzerdaten in einem Format zurück, das für die KI zur Formularausfüllung verwendet werden kann"""
    user = await user_db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    
    form_data = {
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
    
    return form_data

@router.delete("/user/{user_id}")
async def delete_user(user_id: str):
    """Löscht einen Benutzer (Admin-Funktion)"""
    success = await user_db.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    
    return {"message": "Benutzer erfolgreich gelöscht"}

@router.get("/users/stats")
async def get_user_stats():
    """Gibt Statistiken über die registrierten Benutzer zurück"""
    total_users = await user_db.get_user_count()
    return {
        "total_users": total_users,
        "message": f"Insgesamt {total_users} registrierte Benutzer"
    }