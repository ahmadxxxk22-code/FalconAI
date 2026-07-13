from fastapi import APIRouter

from app.ai.multi_timeframe_engine import MultiTimeframeEngine

router = APIRouter(
    prefix="/multi-timeframe",
    tags=["Multi Timeframe"]
)

engine = MultiTimeframeEngine()


@router.get("/{symbol}")
async def analyze(
    symbol: str,
    market: str = "crypto"
):

    return engine.analyze(
        symbol=symbol,
        market=market
    )
