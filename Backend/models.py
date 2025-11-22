# Backend/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    DECIMAL,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from Backend.database import Base   # <-- FIXED: Base must be imported BEFORE models


class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(String(1), default="Y")

    roles = relationship("UserRole", back_populates="user")


class UserRole(Base):
    __tablename__ = "UserRole"

    user_id = Column(Integer, ForeignKey("User.user_id"), primary_key=True)
    role_name = Column(String(20), primary_key=True)

    user = relationship("User", back_populates="roles")


class Organization(Base):
    __tablename__ = "Organization"

    org_id = Column(Integer, primary_key=True, index=True)
    org_name = Column(String(150), nullable=False)
    org_type = Column(String(50), nullable=False)
    address_line1 = Column(String(200))
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))


class Category(Base):
    __tablename__ = "Category"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)
    description = Column(String(255))


class Donation(Base):
    __tablename__ = "Donation"

    donation_id = Column(Integer, primary_key=True, index=True)
    donor_user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    donor_org_id = Column(Integer, ForeignKey("Organization.org_id"))
    category_id = Column(Integer, ForeignKey("Category.category_id"), nullable=False)

    title = Column(String(150), nullable=False, default="Food Donation")
    description = Column(String(500))
    quantity = Column(DECIMAL(10, 2), nullable=False)
    unit = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    available_from = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    pickup_address = Column(String(200))
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))

    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))

    status = Column(String(20), nullable=False, default="AVAILABLE")

    donor_user = relationship("User")
    donor_org = relationship("Organization")
    category = relationship("Category")
