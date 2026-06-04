from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.auth import (
    get_current_user
)

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("/")
async def get_profile(
    current_user=Depends(
        get_current_user
    )
):
    return {
        "success": True,
        "data": {
            "id": current_user["_id"],
            "name": current_user["name"],
            "email": current_user["email"],
            "resume": current_user.get(
                "resume"
            )
        }
    }