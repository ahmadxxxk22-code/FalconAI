from fastapi import FastAPI

from users import router as users_router

from app.ai.signals_engine import SignalEngine
from app.ai.assistant import FalconAssistant

from app.database.base import Base
from app.database.session import engine
import app.database.models

# إنشاء جميع الجداول
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FalconAI",
    description="AI Trading Platform",
    version="1.0.0"
)

app.include_router(users_router)

signal_engine = SignalEngine()
assistant = FalconAssistant()


@app.get("/")
async def home():
    return {
        "status": "online",
        "platform": "FalconAI",
        "version": "1.0.0",
        "message": "Welcome to FalconAI"
    }


@app.get("/health")
async def health():
    return {
        "server": "running",
        "database": "ready",
        "authentication": "ready",
        "ai": "running",
        "signals": "running"
    }


@app.get("/signal/{symbol}")
async def signal(symbol: str, interval: str = "1h"):

    analysis = signal_engine.analyze(
        symbol=symbol,
        interval=interval
    )

    return analysis


@app.get("/assistant/{symbol}")
async def ai(symbol: str, interval: str = "1h"):

    analysis = signal_engine.analyze(
        symbol=symbol,
        interval=interval
    )

    return assistant.explain(analysis)
