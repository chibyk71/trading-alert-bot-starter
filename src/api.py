
from fastapi import FastAPI
from .storage import create_db_and_tables
from .notify.telegram import TelegramNotifier
from .config import settings

app = FastAPI(title="Trading Alert Bot")

@app.on_event("startup")
def startup():
    create_db_and_tables()

@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.ENV}

@app.post("/test-alert")
async def test_alert(message: str = "Hello from bot"):
    TelegramNotifier().send_text(f"TEST: {message}")
    return {"sent": True}
