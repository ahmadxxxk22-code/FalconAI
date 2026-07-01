from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func

from database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Float,
    DateTime
)

from sqlalchemy.sql import func


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(50), unique=True, nullable=False)

    email = Column(String(120), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    full_name = Column(String(120))

    phone = Column(String(30))

    country = Column(String(80))

    language = Column(String(20), default="en")

    timezone = Column(String(50), default="UTC")

    subscription = Column(String(20), default="FREE")

    wallet_balance = Column(Float, default=0)

    is_active = Column(Boolean, default=True)

    is_verified = Column(Boolean, default=False)

    device_id = Column(String(255))

    last_login = Column(DateTime(timezone=True))

    login_count = Column(Integer, default=0)
