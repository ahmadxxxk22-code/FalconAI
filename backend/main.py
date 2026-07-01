from fastapi import FastAPI

from users import router as users_router

app = FastAPI(
    title="FalconAI",
    description="AI Trading Platform",
    version="1.0.0"
)

app.include_router(users_router)


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
        "ai": "coming soon",
        "signals": "coming soon"
    }
