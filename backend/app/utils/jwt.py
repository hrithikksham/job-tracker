from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

ACCESS_TOKEN_MINUTES = 15
REFRESH_TOKEN_DAYS = 7

def create_access_token(user_id: str):

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_MINUTES
    )

    payload = {
        "sub": user_id,
        "type": "access",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def create_refresh_token(user_id: str):

    expire = datetime.utcnow() + timedelta(
        days=REFRESH_TOKEN_DAYS
    )

    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def verify_token(token: str):

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
    