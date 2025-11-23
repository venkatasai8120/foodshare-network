# Backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from Backend.models import User, UserRole
from Backend.schemas import UserCreate, UserLogin, Token, UserOut
from Backend.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)
from Backend.deps import get_db

router = APIRouter()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


@router.post("/register", response_model=UserOut)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    # 1) check if email already exists
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    # 2) create the user
    hashed = get_password_hash(payload.password)
    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hashed,
        phone=payload.phone,
        is_active="Y",
    )
    db.add(user)
    db.flush()  # generates user.user_id

    # 3) create the role record, store ALL CAPS (DONOR / RECEIVER / VOLUNTEER / ADMIN)
    role_name = payload.role.upper()
    role = UserRole(user_id=user.user_id, role_name=role_name)
    db.add(role)

    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    # take first role if multiple
    role = None
    if user.roles:
        role = user.roles[0].role_name

    # include role in JWT (in case we need it later)
    access_token = create_access_token(
        data={"sub": str(user.user_id), "email": user.email, "role": role}
    )

    # 👇 return role in the response so JS can redirect by role
    return Token(access_token=access_token, role=role)


@router.get("/me", response_model=UserOut)
def get_me(token: str, db: Session = Depends(get_db)):
    """
    Simple /auth/me that takes ?token=... (for debugging or future use).
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user
