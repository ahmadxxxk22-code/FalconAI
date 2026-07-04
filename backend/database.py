from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from config import settings

DATABASE_URL = settings.DATABASE_URL

engine_args = {}

if DATABASE_URL.startswith("sqlite"):
    engine_args = {
        "connect_args": {
            "check_same_thread": False
        }
    }

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
    **engine_args
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


def create_database():

    Base.metadata.create_all(
        bind=engine
    )
