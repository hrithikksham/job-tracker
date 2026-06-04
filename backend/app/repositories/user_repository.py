from app.database.mongodb import users_collection
from datetime import datetime


class UserRepository:

    @staticmethod
    async def find_by_email(email: str):
        return await users_collection.find_one(
            {
                "email": email.lower()
            }
        )
    @staticmethod
    async def find_by_phone_number(phone_number: str):
        return await users_collection.find_one(
            {
                "phone_number": phone_number
            }
        )

    @staticmethod
    async def find_by_identifier(identifier: str):
        return await users_collection.find_one(
            {
                "$or": [
                    {"email": identifier.lower()},
                    {"phone_number": identifier}
                ]
            }
        )

    @staticmethod
    async def find_by_id(user_id: str):
        return await users_collection.find_one(
            {
                "_id": user_id
            }
        )

    @staticmethod
    async def create(user_data: dict):
        await users_collection.insert_one(
            user_data
        )

        return user_data

    @staticmethod
    async def update_resume(
        user_id: str,
        resume_data: dict
    ):
        await users_collection.update_one(
            {
                "_id": user_id
            },
            {
                "$set": {
                    "resume": resume_data,
                    "updated_at": datetime.utcnow()
                }
            }
        )

    @staticmethod
    async def update_profile(
        user_id: str,
        update_data: dict
    ):
        await users_collection.update_one(
            {
                "_id": user_id
            },
            {
                "$set": update_data
            }
        )

    @staticmethod
    async def delete(user_id: str):
        await users_collection.delete_one(
            {
                "_id": user_id
            }
        )

    @staticmethod
    async def update_refresh_token(
        user_id: str,
        refresh_token: str
    ):
        await users_collection.update_one(
            {
                "_id": user_id
            },
            {
                "$set": {
                    "refresh_token": refresh_token,
                    "updated_at": datetime.utcnow()
                }
            }
        )