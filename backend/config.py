import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    APP_NAME = os.getenv("APP_NAME", "FalconAI")
    VERSION = os.getenv("VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # ==========================
    # Security
    # ==========================
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "CHANGE_THIS_SECRET_KEY"
    )

    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            60
        )
    )

    # ==========================
    # Database
    # ==========================
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./falconai.db"
    )

    # ==========================
    # Redis
    # ==========================
    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    # ==========================
    # AI
    # ==========================
    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY",
        ""
    )

    NEWS_API_KEY = os.getenv(
        "NEWS_API_KEY",
        ""
    )

    # ==========================
    # Payments
    # ==========================
    NOWPAYMENTS_API_KEY = os.getenv(
        "NOWPAYMENTS_API_KEY",
        ""
    )

    USDT_WALLET = os.getenv(
        "USDT_WALLET",
        ""
    )

    # ==========================
    # Email
    # ==========================
    SMTP_SERVER = os.getenv(
        "SMTP_SERVER",
        ""
    )

    SMTP_PORT = int(
        os.getenv(
            "SMTP_PORT",
            587
        )
    )

    SMTP_USERNAME = os.getenv(
        "SMTP_USERNAME",
        ""
    )

    SMTP_PASSWORD = os.getenv(
        "SMTP_PASSWORD",
        ""
    )


settings = Settings()
