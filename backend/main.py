# backend/main.py

from fastapi import (
    FastAPI,
    Request,
    HTTPException
)

from fastapi.responses import (
    HTMLResponse,
    JSONResponse
)

from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from datetime import datetime

import logging
import traceback


from users import router as users_router

from app.api.multi_timeframe import router as multi_timeframe_router


from app.ai.signals_engine import SignalEngine
from app.ai.assistant import FalconAssistant


from app.database.base import Base
from app.database.session import engine

import app.database.models



# ==================================================
# LOGGING
# ==================================================

logging.basicConfig(

    level=logging.INFO,

    format=
    "%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(
    "FalconAI"
)



# ==================================================
# DATABASE INIT
# ==================================================

try:

    Base.metadata.create_all(
        bind=engine
    )

    logger.info(
        "Database initialized"
    )

except Exception as e:

    logger.error(
        f"Database error: {e}"
    )



# ==================================================
# GLOBAL ENGINES
# ==================================================

signal_engine = None

assistant = None



# ==================================================
# APPLICATION LIFECYCLE
# ==================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    global signal_engine
    global assistant


    try:

        signal_engine = SignalEngine()

        assistant = FalconAssistant()


        logger.info(
            "AI Engines started successfully"
        )


    except Exception as e:

        logger.error(
            f"AI startup failed: {e}"
        )


    yield


    logger.info(
        "FalconAI shutdown"
    )



# ==================================================
# FASTAPI APP
# ==================================================

app = FastAPI(

    title="FalconAI",

    description=
    "Advanced AI Trading Intelligence Platform",

    version="2.0.0",

    lifespan=lifespan

)



# ==================================================
# CORS
# ==================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)



templates = Jinja2Templates(

    directory="templates"

)



# ==================================================
# ROUTERS
# ==================================================

app.include_router(
    users_router
)

app.include_router(
    multi_timeframe_router
)



# ==================================================
# STARTUP / SHUTDOWN
# ==================================================

@app.on_event("startup")
async def startup_event():

    print("===================================")
    print(" FalconAI Starting...")
    print(" Signal Engine Loading...")
    print(" Assistant Loading...")
    print(" Database Connected...")
    print("===================================")


@app.on_event("shutdown")
async def shutdown_event():

    print("===================================")
    print(" FalconAI Shutdown")
    print("===================================")



# ==================================================
# GLOBAL ERROR HANDLER
# ==================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    return {

        "status": "error",

        "message": str(exc),

        "path": request.url.path

    }



# ==================================================
# PLATFORM STATUS
# ==================================================

@app.get("/api/v1/status")
async def platform_status():

    return {

        "platform": "FalconAI",

        "status": "online",

        "version": "1.0.0",

        "engines": {

            "signal_engine": True,

            "risk_manager": True,

            "falcon_assistant": True,

            "multi_timeframe": True

        }

    }



# ==================================================
# MARKET SIGNAL API
# ==================================================

@app.get("/api/v1/signals/{symbol}")
async def get_signal(

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

        "data": result

    }



# ==================================================
# MARKET ANALYSIS API
# ==================================================

@app.get("/api/v1/market/{symbol}")
async def market_analysis(

    symbol: str,

    interval: str = "1h",

    market: str = "crypto"

):

    analysis = signal_engine.market.analyze(

        symbol=symbol,

        interval=interval,

        market=market

    )


    return {

        "status": "success",

        "market": analysis

    }



# ==================================================
# FALCON ASSISTANT API
# ==================================================

@app.get("/api/v1/falcon/chat/{symbol}")
async def falcon_chat(

    symbol: str,

    interval: str = "1h"

):

    analysis = signal_engine.analyze(

        symbol=symbol,

        interval=interval

    )


    response = assistant.explain(

        analysis

    )


    return {

        "status": "success",

        "assistant": response

    }



# ==================================================
# ROOT API INFORMATION
# ==================================================

@app.get("/api/v1")
async def api_root():

    return {

        "name": "FalconAI",

        "description": "AI Trading Platform",

        "version": "1.0.0",

        "status": "running",

        "available_services": [

            "signals",

            "market_analysis",

            "risk_management",

            "falcon_assistant",

            "multi_timeframe"

        ]

    }



# ==================================================
# ENGINE HEALTH CHECK
# ==================================================

@app.get("/api/v1/engine/health")
async def engine_health():

    status = {

        "signal_engine": False,

        "assistant": False,

        "risk_manager": False

    }


    try:

        if signal_engine:

            status["signal_engine"] = True


    except Exception:

        pass



    try:

        if assistant:

            status["assistant"] = True


    except Exception:

        pass



    try:

        if signal_engine.risk:

            status["risk_manager"] = True


    except Exception:

        pass



    return {

        "status": "online",

        "engines": status

    }



# ==================================================
# SIGNAL STATISTICS
# ==================================================

@app.get("/api/v1/statistics")
async def signal_statistics():

    return {

        "statistics":

            signal_engine.signal_statistics

    }



# ==================================================
# QUICK ANALYSIS
# ==================================================

@app.get("/api/v1/quick/{symbol}")
async def quick_analysis(

    symbol: str,

    interval: str = "15m",

    market: str = "crypto"

):

    analysis = signal_engine.analyze(

        symbol=symbol,

        interval=interval,

        market=market

    )


    return {

        "symbol": symbol,

        "signal": analysis.get(

            "direction",

            "WAIT"

        ),

        "confidence": analysis.get(

            "confidence",

            0

        ),

        "price": analysis.get(

            "price",

            0

        )

    }



# ==================================================
# SECURITY / CORS
# ==================================================

from fastapi.middleware.cors import CORSMiddleware


app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "*"

    ],

    allow_credentials=True,

    allow_methods=[

        "*"

    ],

    allow_headers=[

        "*"

    ]

)



# ==================================================
# VERSION INFORMATION
# ==================================================

@app.get("/api/v1/version")
async def version():

    return {

        "platform": "FalconAI",

        "version": "1.0.0",

        "environment": "production",

        "api_status": "active"

    }



# ==================================================
# AVAILABLE MARKETS
# ==================================================

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



# ==================================================
# SYMBOL ANALYSIS CHECK
# ==================================================

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

            "signal": result.get(

                "direction",

                "WAIT"

            ),

            "confidence": result.get(

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



# ==================================================
# USER PROFILE / SUBSCRIPTION STATUS
# ==================================================

@app.get("/api/v1/status")
async def platform_status():

    return {

        "platform": "FalconAI",

        "status": "online",

        "services": {

            "api": True,

            "database": True,

            "signal_engine": True,

            "assistant": True,

            "market_analysis": True,

            "risk_manager": True

        },

        "subscription_system": {

            "enabled": True,

            "plans": [

                "free_trial",

                "monthly",

                "6_months",

                "yearly",

                "enterprise"

            ]

        }

    }



# ==================================================
# GLOBAL ANALYSIS
# ==================================================

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

        "symbol": symbol,

        "interval": interval,

        "market": market,

        "analysis": result

    }



# ==================================================
# AI EXPLANATION
# ==================================================

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

        "symbol": symbol,

        "explanation": explanation,

        "analysis": analysis

    }



# ==================================================
# STARTUP EVENT
# ==================================================

@app.on_event("startup")
async def startup_event():

    print(

        "FalconAI API Started Successfully"

    )

    print(

        "Signal Engine Loaded"

    )

    print(

        "AI Assistant Loaded"

    )



# ==================================================
# SHUTDOWN EVENT
# ==================================================

@app.on_event("shutdown")
async def shutdown_event():

    print(

        "FalconAI API Shutdown"

    )
