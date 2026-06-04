from fastapi import APIRouter, HTTPException, status

from app.schemas.user import (
    UserRegister,
    UserLogin,
    RefreshTokenRequest
)

from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
async def register(
    user_data: UserRegister
):
    try:
        user = await AuthService.register(
            user_data
        )

        return {
            "success": True,
            "message": "User registered successfully",
            "user_id": user["_id"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login")
async def login(
    user_data: UserLogin
):
    try:
        tokens = await AuthService.login(
            user_data
        )

        return {
            "success": True,
            **tokens
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/refresh")
async def refresh_token(
    payload: dict
):
    try:
        refresh_token = payload.get(
            "refresh_token"
        )

        if not refresh_token:
            raise HTTPException(
                status_code=400,
                detail="Refresh token required"
            )

        result = await AuthService.refresh(
            refresh_token
        )

        return {
            "success": True,
            **result
        }

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@router.post("/refresh")
async def refresh_token(
    payload: RefreshTokenRequest
):

    result = await AuthService.refresh(
        payload.refresh_token
    )

    return {
        "success": True,
        **result
    }