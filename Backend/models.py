# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "User"   # existing table name in MySQL

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(CHAR(1), default="Y")

    roles = relationship("UserRole", back_populates="user")


class UserRole(Base):
    __tablename__ = "UserRole"

    user_id = Column(Integer, ForeignKey("User.user_id"), primary_key=True)
    role_name = Column(String(20), primary_key=True)

    user = relationship("User", back_populates="roles")
