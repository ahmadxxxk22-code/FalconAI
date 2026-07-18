# backend/main.py

from fastapi import (
    FastAPI,
    Request
)

from fastapi.responses import (
    HTMLResponse
)

from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

import logging


# ==============================
# ROUTERS
# ==============================

from users import router as users_router

from app.api.multi_timeframe import (
    router as multi_timeframe_router
)


# ==============================
# AI ENGINES
# ==============================

from app.ai.signals_engine import SignalEngine

from app.ai.assistant import FalconAssistant


# ==============================
# DATABASE
# ==============================

from app.database.base import Base

from app.database.session import engine

import app.database.models



# ==============================
# LOGGING
# ==============================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)


logger = logging.getLogger(
    "FalconAI"
)



# ==============================
# DATABASE INIT
# ==============================

try:

    Base.metadata.create_all(
        bind=engine
    )

    logger.info(
        "Database initialized"
    )


except Exception as e:

    logger.error(
        f"Database initialization failed: {e}"
    )



# ==============================
# GLOBAL ENGINES
# ==============================

signal_engine = None

assistant = None



# ==============================
# APPLICATION LIFESPAN
# ==============================

@asynccontextmanager
async def lifespan(app: FastAPI):

    global signal_engine
    global assistant


    try:

        signal_engine = SignalEngine()

        assistant = FalconAssistant()


        logger.info(
            "FalconAI AI Engines loaded"
        )


    except Exception as e:

        logger.error(
            f"AI loading error: {e}"
        )


    yield


    logger.info(
        "FalconAI stopped"
    )



# ==============================
# FASTAPI APP
# ==============================

app = FastAPI(

    title="FalconAI",

    description=
    "Advanced AI Trading Intelligence Platform",

    version="2.0.0",

    lifespan=lifespan

)



# ==============================
# CORS
# ==============================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)



# ==============================
# TEMPLATES
# ==============================

templates = Jinja2Templates(

    directory="templates"

)



# ==============================
# ROUTERS LOAD
# ==============================

app.include_router(
    users_router
)


app.include_router(
    multi_timeframe_router
)



# ==============================
# BASIC STATUS
# ==============================

@app.get("/api/v1/status")
async def platform_status():

    return {

        "platform": "FalconAI",

        "status": "online",

        "version": "2.0.0",

        "engines": {

            "signal_engine": signal_engine is not None,

            "assistant": assistant is not None,

            "multi_timeframe": True

        }

    }



# ==============================
# ROOT API
# ==============================

@app.get("/api/v1")
async def api_root():

    return {

        "name": "FalconAI",

        "description":
            "AI Trading Intelligence Platform",

        "version": "2.0.0",

        "status": "running",

        "services": [

            "signals",

            "market_analysis",

            "assistant",

            "risk_manager",

            "multi_timeframe"

        ]

    }



# ==============================
# SIGNAL ANALYSIS
# ==============================

@app.get("/api/v1/signals/{symbol}")
async def get_signal(

    symbol: str,

    interval: str = "1h",

    market: str = "crypto"

):

    if signal_engine is None:

        return {

            "status": "error",

            "message":
                "Signal Engine not ready"

        }


    result = signal_engine.analyze(

        symbol=symbol,

        interval=interval,

        market=market

    )


    return {

        "status": "success",

        "symbol": symbol,

        "interval": interval,

        "market": market,

        "data": result

    }



# ==============================
# MARKET ANALYSIS
# ==============================

@app.get("/api/v1/market/{symbol}")
async def market_analysis(

    symbol: str,

    interval: str = "1h",

    market: str = "crypto"

):

    if signal_engine is None:

        return {

            "status": "error",

            "message":
                "Engine not ready"

        }


    result = signal_engine.market.analyze(

        symbol=symbol,

        interval=interval,

        market=market

    )


    return {

        "status": "success",

        "market": result

    }



# ==============================
# FALCON ASSISTANT
# ==============================

@app.get("/api/v1/falcon/chat/{symbol}")
async def falcon_chat(

    symbol: str,

    interval: str = "1h"

):

    if signal_engine is None or assistant is None:

        return {

            "status": "error",

            "message":
                "AI services not ready"

        }


    analysis = signal_engine.analyze(

        symbol=symbol,

        interval=interval

    )


    explanation = assistant.explain(

        analysis

    )


    return {

        "status": "success",

        "symbol": symbol,

        "assistant": explanation

    }



# ==============================
# ENGINE HEALTH
# ==============================

@app.get("/api/v1/engine/health")
async def engine_health():

    return {

        "status": "online",

        "engines": {

            "signal_engine":
                signal_engine is not None,

            "assistant":
                assistant is not None,

            "database":
                True

        }

    }



# ==============================
# SIGNAL STATISTICS
# ==============================

@app.get("/api/v1/statistics")
async def signal_statistics():

    if signal_engine is None:

        return {

            "status": "error",

            "message":
                "Signal Engine not ready"

        }


    return {

        "status": "success",

        "statistics":
            getattr(
                signal_engine,
                "signal_statistics",
                {}

            )

    }



# ==============================
# QUICK ANALYSIS
# ==============================

@app.get("/api/v1/quick/{symbol}")
async def quick_analysis(

    symbol: str,

    interval: str = "15m",

    market: str = "crypto"

):

    result = signal_engine.analyze(

        symbol=symbol,

        interval=interval,

        market=market

    )


    return {

        "symbol": symbol,

        "signal":
            result.get(
                "direction",
                result.get(
                    "signal",
                    "WAIT"
                )
            ),

        "confidence":
            result.get(
                "confidence",
                0
            ),

        "price":
            result.get(
                "price",
                0
            )

    }



# ==============================
# FULL ANALYSIS
# ==============================

@app.get("/api/v1/analyze/{symbol}")
async def full_analysis(

    symbol: str,

    interval: str = "1h",

    market: str = "crypto"

):

    result = signal_engine.analyze(

        symbol=symbol,

        interval=interval,

        market=market

    )


    return {

        "status": "success",

        "symbol": symbol,

        "interval": interval,

        "market": market,

        "analysis": result

    }



# ==============================
# AI EXPLANATION
# ==============================

@app.get("/api/v1/explain/{symbol}")
async def explain_signal(

    symbol: str,

    interval: str = "1h",

    market: str = "crypto"

):

    analysis = signal_engine.analyze(

        symbol=symbol,

        interval=interval,

        market=market

    )


    explanation = assistant.explain(

        analysis

    )


    return {

        "status": "success",

        "symbol": symbol,

        "explanation": explanation,

        "analysis": analysis

    }



# ==============================
# VERSION
# ==============================

@app.get("/api/v1/version")
async def version():

    return {

        "platform": "FalconAI",

        "version": "2.0.0",

        "environment":
            "production",

        "api_status":
            "active"

    }



# ==============================
# AVAILABLE MARKETS
# ==============================

@app.get("/api/v1/markets")
async def markets():

    return {

        "markets": [

            "crypto",

            "forex",

            "stocks",

            "gold",

            "oil",

            "indices"

        ],

        "timeframes": [

            "1m",

            "5m",

            "15m",

            "1h",

            "4h",

            "1d",

            "1w",

            "1M"

        ]

    }



# ==============================
# GLOBAL ERROR HANDLER
# ==============================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    logger.error(
        f"Error: {exc}"
    )

    return {

        "status": "error",

        "message": str(exc),

        "path": request.url.path

    }



# ==============================
# ASSISTANT WEB PAGE
# ==============================

@app.get(
    "/assistant",
    response_class=HTMLResponse
)
async def assistant_page(
    request: Request
):

    return templates.TemplateResponse(

        "assistant.html",

        {

            "request": request

        }

    )



# ==============================
# SYMBOL CHECK
# ==============================

@app.get("/api/v1/check/{symbol}")
async def check_symbol(

    symbol: str

):

    try:

        result = signal_engine.analyze(

            symbol=symbol

        )


        return {

            "available": True,

            "symbol": symbol,

            "signal":
                result.get(
                    "signal",
                    "WAIT"
                ),

            "confidence":
                result.get(
                    "confidence",
                    0
                )

        }


    except Exception as e:

        return {

            "available": False,

            "symbol": symbol,

            "error": str(e)

        }



# ==============================
# START MESSAGE
# ==============================

@app.get("/")
async def home():

    return {

        "platform": "FalconAI",

        "status": "online",

        "version": "2.0.0",

        "message":
            "FalconAI API Running"

    }
