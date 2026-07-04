from fastapi import FastAPI
from users import router as users_router

from app.ai.signals_engine import SignalEngine

app = FastAPI(
    title="FalconAI",
    description="AI Trading Platform",
    version="1.0.0"
)

app.include_router(users_router)

engine = SignalEngine()


@app.get("/")
async def home():
    return {
        "status": "online",
        "platform": "FalconAI",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {
        "server": "running",
        "ai": "ready"
    }


@app.get("/ai/analyze/{symbol}")
async def analyze(
    symbol: str,
    interval: str = "1h"
):

    try:

        result = engine.analyze(
            symbol=symbol,
            interval=interval
        )

        return result

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
