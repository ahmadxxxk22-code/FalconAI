from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: str | None = None
    phone: str | None = None
    country: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(user: RegisterRequest):
    return {
        "success": True,
        "message": "User registered successfully",
        "user": {
            "username": user.username,
            "email": user.email
        }
    }


@router.post("/login")
async def login(user: LoginRequest):
    return {
        "success": True,
        "message": "Login successful",
        "token": "coming_soon"
    }


@router.get("/profile")
async def profile():
    return {
        "username": "demo",
        "subscription": "FREE",
        "wallet_balance": 0,
        "signals_used_today": 0
    }
