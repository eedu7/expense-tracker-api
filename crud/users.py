from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import User
from schemas.token import Token
from utils.password import get_password_hash, verify_password
from utils.jwt import encode_token

def get_all(db: Session):
    try:
        return db.query(User).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def get_by_email(db: Session, email: str) -> User | None:
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not able to query data. ({e})",
        )


def register_user(db: Session, user_data: dict) -> bool:
    user = get_by_email(db, email=user_data["email"])
    if user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "User with this email already exists."
        )
    try:
        user_data["password"] = get_password_hash(user_data["password"])
        new_user = User(**user_data)
        db.add(new_user)
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, f"Not able to register user. ({e})"
        )


def login_user(db: Session, user_data: dict) -> Token:
    user = get_by_email(db, email=user_data.get("email"))
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User does not exist.")
    if not verify_password(user_data.get("password"), user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials.")
    data = {
        "user_id": user.id,
        "email": user.email,
        "type": "access-token"
    }
    access_token, exp = encode_token(data)
    data = {
        "user_id": user.id,
        "email": user.email,
        "type": "refresh-token"
    }
    refresh_token, exp = encode_token(data)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        exp=exp
    )

