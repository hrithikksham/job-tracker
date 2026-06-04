from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ResumeInfo(BaseModel):
    file_id: str
    filename: str
    uploaded_at: datetime


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    password: str


class UserLogin(BaseModel):
    identifier: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone_number: str
    resume: Optional[ResumeInfo] = None
    created_at: datetime