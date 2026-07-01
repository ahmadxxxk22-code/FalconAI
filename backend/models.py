from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime
)
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


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(50), unique=True, nullable=False, index=True)

    email = Column(String(120), unique=True, nullable=False, index=True)

    password = Column(String(255), nullable=False)

    full_name = Column(String(120))

    phone = Column(String(30))

    country = Column(String(80))

    language = Column(String(20), default="en")

    timezone = Column(String(50), default="UTC")

    subscription = Column(String(30), default="FREE")

    wallet_balance = Column(Float, default=0)

    is_active = Column(Boolean, default=True)

    is_verified = Column(Boolean, default=False)

    device_id = Column(String(255))

    referral_code = Column(String(50), unique=True)

    referred_by = Column(String(50))

    login_count = Column(Integer, default=0)

    last_login = Column(DateTime(timezone=True))


class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    user_id = Column(Integer, nullable=False, index=True)

    plan = Column(String(30), default="FREE")

    status = Column(String(30), default="ACTIVE")

    payment_method = Column(String(50))

    amount = Column(Float, default=0)

    currency = Column(String(10), default="USD")

    start_date = Column(DateTime(timezone=True), server_default=func.now())

    end_date = Column(DateTime(timezone=True))

    auto_renew = Column(Boolean, default=False)

    transaction_id = Column(String(255))


class Payment(BaseModel):
    __tablename__ = "payments"

    user_id = Column(Integer, nullable=False, index=True)

    subscription_id = Column(Integer)

    amount = Column(Float, nullable=False)

    currency = Column(String(10), default="USD")

    payment_method = Column(String(50))

    provider = Column(String(50))

    transaction_id = Column(String(255), unique=True)

    status = Column(String(30), default="PENDING")

    invoice_number = Column(String(100))

    paid_at = Column(DateTime(timezone=True))

    notes = Column(String(255))
