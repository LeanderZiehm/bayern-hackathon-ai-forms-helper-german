import os
from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid
from dotenv import load_dotenv

load_dotenv()

class SimpleUserDatabase:
    """Einfache In-Memory-Datenbank als Fallback, wenn MongoDB nicht verfügbar ist"""
    def __init__(self):
        self.users = {}
        self._create_sample_user()
    
    def _create_sample_user(self):
        """Erstellt einen Beispielbenutzer für Tests"""
        sample_user_id = "sample-user-123"
        self.users[sample_user_id] = {
            "_id": sample_user_id,
            "first_name": "Max",
            "last_name": "Mustermann",
            "email": "max.mustermann@example.com",
            "phone": "+49 123 456789",
            "street": "Musterstraße",
            "house_number": "123",
            "postal_code": "80331",
            "city": "München",
            "country": "Deutschland",
            "birth_date": "1990-01-01",
            "birth_place": "München",
            "nationality": "Deutsch",
            "marital_status": "ledig",
            "occupation": "Softwareentwickler",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    
    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """Erstellt einen neuen Benutzer"""
        user_id = str(uuid.uuid4())
        
        # Prüfen ob E-Mail bereits existiert
        for existing_user in self.users.values():
            if existing_user.get('email') == user_data.get('email'):
                raise ValueError("E-Mail-Adresse bereits registriert")
        
        user_doc = {
            "_id": user_id,
            **user_data,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        self.users[user_id] = user_doc
        return user_id
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Lädt einen Benutzer anhand der ID"""
        user_doc = self.users.get(user_id)
        if user_doc:
            # Kopie ohne _id zurückgeben
            user_copy = user_doc.copy()
            user_copy.pop("_id", None)
            return user_copy
        return None
    
    async def update_user(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """Aktualisiert einen Benutzer"""
        if user_id in self.users:
            user_data["updated_at"] = datetime.now()
            self.users[user_id].update(user_data)
            return True
        return False
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Lädt einen Benutzer anhand der E-Mail-Adresse"""
        for user in self.users.values():
            if user.get('email') == email:
                user_copy = user.copy()
                user_copy.pop("_id", None)
                return user_copy
        return None
    
    async def get_all_users(self) -> List[Dict[str, Any]]:
        """Lädt alle Benutzer"""
        users = []
        for user_doc in self.users.values():
            user_copy = user_doc.copy()
            user_copy.pop("_id", None)
            users.append(user_copy)
        return users
    
    async def delete_user(self, user_id: str) -> bool:
        """Löscht einen Benutzer"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    async def get_user_count(self) -> int:
        """Gibt die Anzahl der registrierten Benutzer zurück"""
        return len(self.users)

# Versuche MongoDB zu verwenden, falls verfügbar
try:
    from services.mongodb_database import MongoDBUserDatabase
    user_db = MongoDBUserDatabase()
    print("✅ MongoDB-Verbindung erfolgreich")
except Exception as e:
    print(f"⚠️ MongoDB nicht verfügbar: {e}")
    print("🔄 Verwende einfache In-Memory-Datenbank")
    user_db = SimpleUserDatabase()
