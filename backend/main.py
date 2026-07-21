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

from app.notifications.router import (
    router as notifications_router
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

app.include_router(
    notifications_router
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



# =====================================================
# FALCON ASSISTANT API
# =====================================================


@app.get(
    "/api/v1/falcon/chat/{symbol}"
)
async def falcon_chat(

    symbol: str,

    interval: str = "1h",

    market: str = "crypto"

):


    if signal_engine is None or assistant is None:


        return {


            "status":

                "error",


            "message":

                "AI services not ready"


        }



    try:


        analysis = signal_engine.analyze(

            symbol=symbol,

            interval=interval,

            market=market

        )



        explanation = assistant.explain(

            analysis

        )



        return {


            "status":

                "success",


            "symbol":

                symbol,


            "assistant":

                explanation


        }



    except Exception as e:


        logger.exception(

            f"Assistant error: {e}"

        )


        return {


            "status":

                "error",


            "message":

                str(e)


        }




# =====================================================
# SIGNAL STATISTICS
# =====================================================


@app.get(
    "/api/v1/statistics"
)
async def signal_statistics():


    if signal_engine is None:


        return {


            "status":

                "error",


            "message":

                "Signal Engine not ready"


        }



    return {


        "status":

            "success",


        "statistics":

            getattr(

                signal_engine,

                "signal_statistics",

                {}

            )


    }




# =====================================================
# AVAILABLE MARKETS
# =====================================================


@app.get(
    "/api/v1/markets"
)
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




# =====================================================
# QUICK ANALYSIS
# =====================================================


@app.get(
    "/api/v1/quick/{symbol}"
)
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


        "symbol":

            symbol,


        "signal":

            result.get(

                "signal",

                "WAIT"

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



# =====================================================
# AI EXPLANATION API
# =====================================================


@app.get(
    "/api/v1/explain/{symbol}"
)
async def explain_signal(

    symbol: str,

    interval: str = "1h",

    market: str = "crypto"

):


    if signal_engine is None or assistant is None:


        return {


            "status":

                "error",


            "message":

                "AI services not ready"


        }



    try:


        analysis = signal_engine.analyze(

            symbol=symbol,

            interval=interval,

            market=market

        )



        explanation = assistant.explain(

            analysis

        )



        return {


            "status":

                "success",


            "symbol":

                symbol,


            "explanation":

                explanation,


            "analysis":

                analysis


        }



    except Exception as e:


        logger.exception(

            f"Explanation error: {e}"

        )


        return {


            "status":

                "error",


            "message":

                str(e)


        }




# =====================================================
# SYMBOL AVAILABILITY CHECK
# =====================================================


@app.get(
    "/api/v1/check/{symbol}"
)
async def check_symbol(

    symbol: str

):


    try:


        if signal_engine is None:


            return {


                "available":

                    False,


                "symbol":

                    symbol,


                "error":

                    "Engine not ready"


            }



        result = signal_engine.analyze(

            symbol=symbol

        )



        return {


            "available":

                True,


            "symbol":

                symbol,


            "signal":

                result.get(

                    "signal",

                    result.get(

                        "direction",

                        "WAIT"

                    )

                ),


            "confidence":

                result.get(

                    "confidence",

                    0

                )


        }



    except Exception as e:


        return {


            "available":

                False,


            "symbol":

                symbol,


            "error":

                str(e)


        }




# =====================================================
# GLOBAL ERROR HANDLER
# =====================================================


@app.exception_handler(
    Exception
)
async def global_exception_handler(

    request: Request,

    exc: Exception

):


    logger.exception(

        f"Unhandled error: {exc}"

    )


    return JSONResponse(

        status_code=500,


        content={


            "status":

                "error",


            "message":

                str(exc),


            "path":

                request.url.path


        }

    )




# =====================================================
# ASSISTANT WEB PAGE
# =====================================================


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


            "request":

                request


        }

    )




# =====================================================
# HOME
# =====================================================


@app.get(
    "/"
)
async def home():


    return {


        "platform":

            APP_NAME,


        "status":

            "online",


        "version":

            APP_VERSION,


        "message":

            "FalconAI API Running"


    }
