import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "FalconAI"
    VERSION = "1.0.0"

    SECRET_KEY = os.getenv("SECRET_KEY")

    DATABASE_URL = os.getenv("DATABASE_URL")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

settings = Settings()
