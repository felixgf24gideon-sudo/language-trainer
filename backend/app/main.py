from fastapi import FastAPI
from app.database.db import initialize_database

app = FastAPI(title="Language Trainer API", version="1.0.0")

@app.on_event("startup")
async def startup():
    initialize_database()

@app.get("/health")
async def health():
    return {"status": "ok"}
