from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.password import hash_password
from app.utils.password import verify_password
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token
)


class AuthService:

    @staticmethod
    async def register(data):

        existing = await UserRepository.find_by_email(
            data.email
        )

        if existing:
            raise Exception(
                "Email already exists"
            )

        existing = await UserRepository.find_by_phone_number(
            data.phone_number
        )   

        if existing:
            raise Exception(
                "Phone number already exists"
            )

        user = User.create(
            name=data.name,
            email=data.email,
            phone_number=data.phone_number,
            password_hash=hash_password(
                data.password
            )
        )

        await UserRepository.create(user)

        return user

    @staticmethod
    async def login(data):
        user = await UserRepository.find_by_identifier(
            data.identifier
        )
        
        if not user:
            raise Exception(
            "Invalid credentials"
                )

        valid = verify_password(
            data.password,
            user["password_hash"]
            )

        if not valid:
            raise Exception(
                "Invalid Password"
            )

        access_token = create_access_token(user["_id"])
        refresh_token = create_refresh_token(user["_id"])


        await UserRepository.update_refresh_token(
            user["_id"],
            refresh_token
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    @staticmethod
    async def refresh(refresh_token: str):

        payload = verify_token(refresh_token)

        if payload["type"] != "refresh":
            raise Exception(
                "Invalid token type"
            )

        user = await UserRepository.find_by_id(
            payload["sub"]
        )

        if not user:
            raise Exception(
                "User not found"
            )

        if user["refresh_token"] != refresh_token:
            raise Exception(
                "Invalid refresh token"
            )

        access_token = create_access_token(
            user["_id"]
        )

        return {
            "access_token": access_token
        }
