from fastapi import APIRouter
from app.services.signal_engine import SignalEngine

router = APIRouter(
    prefix="/signals",
    tags=["Signals"]
)

engine = SignalEngine()


@router.get("/")
async def get_signals():
    return {
        "success": True,
        "message": "Signals system active"
    }


@router.get("/timeframes")
async def get_timeframes():
    return {
        "success": True,
        "timeframes": [
            "1m", "5m", "15m", "30m",
            "1h", "4h", "1d"
        ]
    }


@router.get("/markets")
async def get_markets():
    return {
        "success": True,
        "markets": [
            "Crypto",
            "Forex",
            "Stocks",
            "Gold",
            "Silver",
            "Oil",
            "Indices"
        ]
    }


# 🔥 هذا أهم endpoint الآن
@router.get("/analyze")
async def analyze(symbol: str = "BTCUSDT", timeframe: str = "1m"):
    result = engine.analyze_market(symbol, timeframe)

    return {
        "success": True,
        "signal": result
    }


@router.post("/generate")
async def generate_signal(symbol: str = "BTCUSDT", timeframe: str = "1m"):
    result = engine.analyze_market(symbol, timeframe)

    return {
        "success": True,
        "message": "Signal generated successfully",
        "signal": result
    }


@router.get("/{signal_id}")
async def signal_details(signal_id: int):
    return {
        "success": True,
        "signal_id": signal_id
    }


@router.post("/{signal_id}/close")
async def close_signal(signal_id: int):
    return {
        "success": True,
        "message": "Signal closed",
        "signal_id": signal_id
    }
