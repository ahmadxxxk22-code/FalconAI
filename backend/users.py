from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.auth.auth_service import AuthService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: str = ""
    phone: str = ""
    country: str = ""


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    auth = AuthService(db)

    user = auth.register(
        username=request.username,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        phone=request.phone,
        country=request.country
    )

    return {
        "success": True,
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    }


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    auth = AuthService(db)

    return auth.login(
        email=request.email,
        password=request.password
    )


@router.get("/profile/{user_id}")
def profile(
    user_id: int,
    db: Session = Depends(get_db)
):

    auth = AuthService(db)

    user = auth.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "subscription": user.subscription.plan if user.subscription else "FREE"
    }


@router.get("/ping")
def ping():

    return {
        "status": "ok"
    }
