from fastapi import HTTPException, status

from models import User
from sqlalchemy.orm import Session

from utils.password import get_password_hash


def get_by_email(db: Session, email: str) -> User | None:
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not able to query data. ({e})"
        )

def register_user(db: Session, user: dict) -> bool:
    exist = get_by_email(db, email=user['email'])
    if exist:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "User with this email already exists."
        )
    try:
        user["password"] = get_password_hash(user["password"])
        new_user = User(**user)
        db.add(new_user)
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Not able to register user. ({e})"
        )

