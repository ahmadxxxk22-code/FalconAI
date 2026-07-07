from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, index=True)

    email = Column(String(150), unique=True, index=True)

    password = Column(String(255))

    full_name = Column(String(150))

    phone = Column(String(50))

    country = Column(String(80))

    is_active = Column(Boolean, default=True)

    is_admin = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    subscription = relationship(
        "Subscription",
        back_populates="user",
        uselist=False
    )

    signals = relationship(
        "SignalHistory",
        back_populates="user"
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    plan = Column(String(30), default="FREE")

    expires_at = Column(DateTime)

    active = Column(Boolean, default=True)

    user = relationship(
        "User",
        back_populates="subscription"
    )


class SignalHistory(Base):
    __tablename__ = "signal_history"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    symbol = Column(String(30))

    interval = Column(String(20))

    direction = Column(String(20))

    confidence = Column(Float)

    price = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="signals"
    )


class LoginSession(Base):
    __tablename__ = "login_sessions"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    token = Column(String(500))

    device = Column(String(200))

    ip = Column(String(100))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    exchange = Column(String(50))

    api_key = Column(String(255))

    secret_key = Column(String(255))

    active = Column(Boolean, default=True)
