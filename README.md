
``
# Bayern Hackathon AI Forms Helper German

Eine KI-gestützte Web-Anwendung, die beim Ausfüllen deutscher Behördenformulare hilft.

## Features

- 📋 **Formular-Browser**: Durchsuche verfügbare deutsche Formulare
- 🤖 **KI-Chat**: Intelligenter Assistent mit Groq Llama-3.3-70b
- 👤 **Benutzerregistrierung**: Personalisierte Hilfe mit gespeicherten Daten
- 📄 **PDF-Viewer**: Integrierter PDF-Viewer
- 🔄 **Automatisches Ausfüllen**: KI nutzt deine Daten für Formularvorschläge

## Installation

### 1. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 2. MongoDB einrichten

#### Option A: Lokale MongoDB-Installation
1. MongoDB installieren: https://www.mongodb.com/try/download/community
2. MongoDB-Service starten
3. Standard-Verbindung: `mongodb://localhost:27017`

#### Option B: MongoDB Atlas (Cloud)
1. Account erstellen: https://www.mongodb.com/atlas
2. Cluster erstellen
3. Verbindungsstring kopieren

### 3. Umgebungsvariablen einrichten

Erstelle eine `.env`-Datei im Projektverzeichnis:

```env
# Groq API Key
GROQ_API_KEY=dein_groq_api_schlüssel_hier

# MongoDB Konfiguration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=bayern_formular_helper

# Alternative für MongoDB Atlas:
# MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
```

### 4. Server starten
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 5012
```

### 5. Anwendung öffnen
Öffne deinen Browser und gehe zu: `http://localhost:5012`

## Verwendung

1. **Registrierung**: Erstelle ein Benutzerkonto mit deinen Daten
2. **Formular auswählen**: Wähle ein Formular aus der Liste
3. **KI-Hilfe**: Stelle Fragen zur Formularausfüllung
4. **Personalisierung**: Gib deine Benutzer-ID ein für personalisierte Hilfe

## API-Endpunkte

- `POST /register` - Benutzerregistrierung
- `GET /user/{user_id}` - Benutzerdaten abrufen
- `PUT /user/{user_id}` - Benutzerdaten aktualisieren
- `POST /chat` - KI-Chat mit optionaler Personalisierung
- `GET /pdfs` - Verfügbare Formulare auflisten
- `GET /users/stats` - Benutzerstatistiken

## Technologie-Stack

- **Backend**: FastAPI, Python
- **Datenbank**: MongoDB mit Motor (async)
- **KI**: Groq API mit Llama-3.3-70b
- **Frontend**: HTML, CSS, JavaScript
- **PDF-Verarbeitung**: PyMuPDF

## Entwicklung

Das Projekt verwendet:
- Async/await für bessere Performance
- MongoDB für skalierbare Datenspeicherung
- Pydantic für Datenvalidierung
- CORS für Frontend-Integration