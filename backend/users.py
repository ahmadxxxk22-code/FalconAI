from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
async def get_users():
    return {
        "status": "success",
        "message": "Users endpoint is working",
        "data": []
    }


@router.get("/profile")
async def profile():
    return {
        "status": "success",
        "message": "Profile endpoint"
    }
