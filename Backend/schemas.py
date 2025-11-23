# Backend/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# -------------------------
# USER SCHEMAS
# -------------------------


class UserCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str
    role: str  # "DONOR", "RECEIVER", "VOLUNTEER", "ADMIN" (we'll send uppercase)


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    user_id: int
    full_name: str
    email: str
    phone: str
    is_active: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    # 👇 NEW: backend will now send the role in login response
    role: Optional[str] = None


# -------------------------
# DONATION SCHEMAS
# -------------------------


class DonationCreate(BaseModel):
    category_id: int
    description: str
    quantity: float
    unit: str
    expires_at: datetime
    pickup_address: str
    city: str
    state: str
    zip_code: str


class DonationOut(BaseModel):
    donation_id: int
    donor_user_id: int
    category_id: int
    description: str
    quantity: float
    unit: str
    status: str
    expires_at: datetime
    pickup_address: str
    city: str
    state: str
    zip_code: str

    class Config:
        orm_mode = True
