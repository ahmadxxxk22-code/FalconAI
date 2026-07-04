from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


fake_users = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@falconai.com",
        "subscription": "PRO"
    }
]


@router.get("/")
async def get_users():

    return {
        "status": "success",
        "count": len(fake_users),
        "users": fake_users
    }


@router.get("/{user_id}")
async def get_user(user_id: int):

    for user in fake_users:

        if user["id"] == user_id:
            return {
                "status": "success",
                "user": user
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


@router.get("/profile/me")
async def profile():

    return {
        "status": "success",
        "profile": {
            "username": "admin",
            "subscription": "PRO",
            "wallet_balance": 0,
            "language": "en"
        }
    }


@router.get("/ping")
async def ping():

    return {
        "status": "success",
        "message": "Users API is working"
    }
