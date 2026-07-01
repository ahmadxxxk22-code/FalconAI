import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = "FalconAI"
    VERSION = "1.0.0"

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Redis
    REDIS_URL = os.getenv("REDIS_URL")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # News API
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

    # Crypto Payments
    NOWPAYMENTS_API_KEY = os.getenv("NOWPAYMENTS_API_KEY")
    USDT_WALLET = os.getenv("USDT_WALLET")

    # Email
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = os.getenv("SMTP_PORT")
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


settings = Settings()
