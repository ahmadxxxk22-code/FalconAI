from fastapi import APIRouter

router = APIRouter()

@router.get("/profile")
async def profile():
    return {"message": "User Profile"}
