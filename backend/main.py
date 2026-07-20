# backend/main.py


# =====================================================
# STANDARD LIBRARIES
# =====================================================

from datetime import datetime

from typing import (
    Dict,
    Any
)

from contextlib import (
    asynccontextmanager
)

import logging

import os



# =====================================================
# FASTAPI IMPORTS
# =====================================================

from fastapi import (
    FastAPI,
    Request
)


from fastapi.responses import (
    HTMLResponse,
    JSONResponse
)


from fastapi.templating import (
    Jinja2Templates
)


from fastapi.middleware.cors import (
    CORSMiddleware
)




# =====================================================
# APPLICATION CONFIGURATION
# =====================================================


APP_NAME = "FalconAI"

APP_VERSION = "3.0.0"

APP_ENV = os.getenv(
    "APP_ENV",
    "production"
)


DEBUG_MODE = (
    APP_ENV != "production"
)




# =====================================================
# LOGGING CONFIGURATION
# =====================================================


logging.basicConfig(

    level=(
        logging.DEBUG
        if DEBUG_MODE
        else logging.INFO
    ),


    format=(

        "%(asctime)s | "

        "%(levelname)s | "

        "%(name)s | "

        "%(message)s"

    )

)



logger = logging.getLogger(
    APP_NAME
)




# =====================================================
# ROUTERS
# =====================================================


from users import (
    router as users_router
)



from app.api.multi_timeframe import (
    router as multi_timeframe_router
)




# =====================================================
# AI ENGINES
# =====================================================


from app.ai.signals_engine import (
    SignalEngine
)



from app.ai.assistant import (
    FalconAssistant
)




# =====================================================
# DATABASE
# =====================================================


from app.database.base import (
    Base
)


from app.database.session import (
    engine
)


import app.database.models




# =====================================================
# DATABASE INITIALIZATION
# =====================================================


try:


    Base.metadata.create_all(

        bind=engine

    )


    logger.info(

        "Database initialized successfully"

    )


except Exception as e:


    logger.error(

        f"Database initialization failed: {e}"

    )




# =====================================================
# GLOBAL AI INSTANCES
# =====================================================


signal_engine = None


assistant = None



# =====================================================
# APPLICATION LIFESPAN
# =====================================================


@asynccontextmanager
async def lifespan(
    app: FastAPI
):


    global signal_engine

    global assistant



    try:


        logger.info(

            "Starting FalconAI engines..."

        )



        signal_engine = SignalEngine()



        assistant = FalconAssistant()



        logger.info(

            "FalconAI engines loaded successfully"

        )



    except Exception as e:


        logger.exception(

            f"Engine startup failed: {e}"

        )



    yield



    logger.info(

        "FalconAI shutdown completed"

    )




# =====================================================
# FASTAPI APPLICATION
# =====================================================


app = FastAPI(


    title=APP_NAME,


    description=(

        "Advanced AI Trading Intelligence Platform"

    ),


    version=APP_VERSION,


    lifespan=lifespan

)



# =====================================================
# CORS CONFIGURATION
# =====================================================


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




# =====================================================
# TEMPLATES
# =====================================================


templates = Jinja2Templates(

    directory="templates"

)




# =====================================================
# ROUTERS REGISTRATION
# =====================================================


app.include_router(

    users_router

)



app.include_router(

    multi_timeframe_router

)




# =====================================================
# PLATFORM STATUS
# =====================================================


@app.get(
    "/api/v1/status"
)
async def platform_status():


    return {


        "platform":

            APP_NAME,


        "status":

            "online",


        "version":

            APP_VERSION,


        "environment":

            APP_ENV,


        "engines": {


            "signal_engine":

                signal_engine is not None,


            "assistant":

                assistant is not None,


            "multi_timeframe":

                True


        }


    }




# =====================================================
# API ROOT
# =====================================================


@app.get(
    "/api/v1"
)
async def api_root():


    return {


        "name":

            APP_NAME,


        "description":

            "AI Trading Intelligence Platform",


        "version":

            APP_VERSION,


        "status":

            "running",


        "services": [


            "signals",


            "market_analysis",


            "assistant",


            "risk_manager",


            "multi_timeframe",


            "economic_intelligence"


        ]

    }




# =====================================================
# ENGINE HEALTH CHECK
# =====================================================


@app.get(
    "/api/v1/engine/health"
)
async def engine_health():


    return {


        "status":

            "online",


        "engines": {


            "signal_engine":

                signal_engine is not None,


            "assistant":

                assistant is not None,


            "database":

                True


        },


        "timestamp":

            datetime.utcnow().isoformat()


    }




# =====================================================
# VERSION INFO
# =====================================================


@app.get(
    "/api/v1/version"
)
async def version():


    return {


        "platform":

            APP_NAME,


        "version":

            APP_VERSION,


        "environment":

            APP_ENV,


        "api_status":

            "active"


}



# =====================================================
# SIGNAL ANALYSIS API
# =====================================================


@app.get(
    "/api/v1/signals/{symbol}"
)
async def get_signal(

    symbol: str,

    interval: str = "1h",

    market: str = "crypto"

):


    if signal_engine is None:


        return {


            "status":

                "error",


            "message":

                "Signal Engine not ready"


        }



    try:


        result = signal_engine.analyze(

            symbol=symbol,

            interval=interval,

            market=market

        )


        return {


            "status":

                "success",


            "symbol":

                symbol,


            "interval":

                interval,


            "market":

                market,


            "data":

                result


        }



    except Exception as e:


        logger.exception(

            f"Signal analysis error: {e}"

        )


        return {


            "status":

                "error",


            "message":

                str(e)


        }




# =====================================================
# MARKET ANALYSIS API
# =====================================================


@app.get(
    "/api/v1/market/{symbol}"
)
async def market_analysis(

    symbol: str,

    interval: str = "1h",

    market: str = "crypto"

):


    if signal_engine is None:


        return {


            "status":

                "error",


            "message":

                "Engine not ready"


        }



    try:


        result = signal_engine.market.analyze(

            symbol=symbol,

            interval=interval,

            market=market

        )


        return {


            "status":

                "success",


            "symbol":

                symbol,


            "market":

                market,


            "analysis":

                result


        }



    except Exception as e:


        logger.exception(

            f"Market analysis error: {e}"

        )


        return {


            "status":

                "error",


            "message":

                str(e)


        }




# =====================================================
# FULL AI ANALYSIS
# =====================================================


@app.get(
    "/api/v1/analyze/{symbol}"
)
async def full_analysis(

    symbol: str,

    interval: str = "1h",

    market: str = "crypto"

):


    if signal_engine is None:


        return {


            "status":

                "error",


            "message":

                "Signal Engine not ready"


        }



    result = signal_engine.analyze(

        symbol=symbol,

        interval=interval,

        market=market

    )



    return {


        "status":

            "success",


        "analysis":

            result


    }
