import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
import uuid
from dotenv import load_dotenv

load_dotenv()

class MongoDBUserDatabase:
    def __init__(self):
        # MongoDB-Verbindung
        self.mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        self.database_name = os.getenv("MONGODB_DATABASE", "bayern_formular_helper")
        self.collection_name = "users"
        
        # Client und Datenbank initialisieren
        self.client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]
        
        # Index für E-Mail erstellen (eindeutig) - synchron beim Start
        # self._create_indexes()  # Entfernt, da es async ist
    
    async def _create_indexes(self):
        """Erstellt notwendige Indizes für die Datenbank"""
        try:
            # Eindeutiger Index für E-Mail
            await self.collection.create_index("email", unique=True)
            # Index für bessere Performance
            await self.collection.create_index("created_at")
        except Exception as e:
            print(f"Fehler beim Erstellen der Indizes: {e}")
    
    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """Erstellt einen neuen Benutzer in der Datenbank"""
        user_id = str(uuid.uuid4())
        
        # Benutzerdaten vorbereiten
        user_doc = {
            "_id": user_id,
            **user_data,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        try:
            await self.collection.insert_one(user_doc)
            return user_id
        except DuplicateKeyError:
            raise ValueError("E-Mail-Adresse bereits registriert")
        except Exception as e:
            raise ValueError(f"Fehler beim Erstellen des Benutzers: {str(e)}")
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Lädt einen Benutzer anhand der ID"""
        try:
            user_doc = await self.collection.find_one({"_id": user_id})
            if user_doc:
                # MongoDB-spezifische Felder entfernen
                user_doc.pop("_id", None)
                return user_doc
            return None
        except Exception as e:
            print(f"Fehler beim Laden des Benutzers: {e}")
            return None
    
    async def update_user(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """Aktualisiert einen Benutzer"""
        try:
            # updated_at hinzufügen
            user_data["updated_at"] = datetime.now()
            
            result = await self.collection.update_one(
                {"_id": user_id},
                {"$set": user_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Fehler beim Aktualisieren des Benutzers: {e}")
            return False
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Lädt einen Benutzer anhand der E-Mail-Adresse"""
        try:
            user_doc = await self.collection.find_one({"email": email})
            if user_doc:
                user_doc.pop("_id", None)
                return user_doc
            return None
        except Exception as e:
            print(f"Fehler beim Laden des Benutzers per E-Mail: {e}")
            return None
    
    async def get_all_users(self) -> List[Dict[str, Any]]:
        """Lädt alle Benutzer (für Admin-Zwecke)"""
        try:
            users = []
            async for user_doc in self.collection.find():
                user_doc.pop("_id", None)
                users.append(user_doc)
            return users
        except Exception as e:
            print(f"Fehler beim Laden aller Benutzer: {e}")
            return []
    
    async def delete_user(self, user_id: str) -> bool:
        """Löscht einen Benutzer"""
        try:
            result = await self.collection.delete_one({"_id": user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Fehler beim Löschen des Benutzers: {e}")
            return False
    
    async def search_users(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Sucht Benutzer nach verschiedenen Kriterien"""
        try:
            users = []
            async for user_doc in self.collection.find(query):
                user_doc.pop("_id", None)
                users.append(user_doc)
            return users
        except Exception as e:
            print(f"Fehler bei der Benutzersuche: {e}")
            return []
    
    async def get_user_count(self) -> int:
        """Gibt die Anzahl der registrierten Benutzer zurück"""
        try:
            return await self.collection.count_documents({})
        except Exception as e:
            print(f"Fehler beim Zählen der Benutzer: {e}")
            return 0
    
    async def close_connection(self):
        """Schließt die MongoDB-Verbindung"""
        self.client.close()

# Globale Datenbankinstanz
user_db = MongoDBUserDatabase()
