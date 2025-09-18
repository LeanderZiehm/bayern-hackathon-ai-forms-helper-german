from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes import chat, files, upload

app = FastAPI(title="Groq Llama-3.3-70b API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Include routes
app.include_router(chat.router)
app.include_router(files.router)
app.include_router(upload.router) 


from fastapi.responses import FileResponse

@app.get("/")
async def root():
    return FileResponse("static/index.html")
