from fastapi import FastAPI

app = FastAPI(title="FalconAI Backend")

@app.get("/")
def home():
    return {"message": "FalconAI is running 🚀"}
