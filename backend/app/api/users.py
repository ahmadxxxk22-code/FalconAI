from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
async def get_users():
    return {
        "success": True,
        "message": "Users list endpoint"
    }


@router.get("/{user_id}")
async def get_user(user_id: int):
    return {
        "success": True,
        "user_id": user_id
    }


@router.post("/register")
async def register():
    return {
        "success": True,
        "message": "Register endpoint"
    }


@router.post("/login")
async def login():
    return {
        "success": True,
        "message": "Login endpoint"
    }


@router.put("/{user_id}")
async def update_user(user_id: int):
    return {
        "success": True,
        "message": "User updated",
        "user_id": user_id
    }


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    return {
        "success": True,
        "message": "User deleted",
        "user_id": user_id
    }
