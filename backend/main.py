from fastapi import FastAPI

app = FastAPI(
    title="FalconAI",
    description="AI Trading Platform",
    version="1.0.0"
)

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
        "database": "coming soon",
        "ai": "coming soon"
    }
