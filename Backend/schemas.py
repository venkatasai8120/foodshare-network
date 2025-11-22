# backend/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional


class Role(BaseModel):
    role_name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str
    roles: Optional[List[str]] = ["DONOR"]


class UserOut(UserBase):
    user_id: int
    is_active: str
    roles: List[Role] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
