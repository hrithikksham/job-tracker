from datetime import datetime
from uuid import uuid4


class User:
    @staticmethod
    def create(
        name: str,
        email: str,
        phone_number: str,
        password_hash: str
    ):
        now = datetime.utcnow()

        return {
            "_id": str(uuid4()),
            "name": name,
            "email": email.lower(),
            "phone_number": phone_number,
            "password_hash": password_hash,
            "resume": None,
            "refresh_token": None,
            "created_at": now,
            "updated_at": now
        }

    @staticmethod
    def resume_metadata(
        file_id: str,
        filename: str
    ):
        return {
            "file_id": file_id,
            "filename": filename,
            "uploaded_at": datetime.utcnow()
        }