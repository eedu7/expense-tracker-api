from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud.users as crud_users
from database import get_db
from schemas import LoginUser, RegisterUser

router = APIRouter()


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return crud_users.get_all(db)


@router.post("/register")
def register_user(user_data: RegisterUser, db: Session = Depends(get_db)):
    return crud_users.register_user(db, user_data.model_dump())


@router.post("/login")
def login_user(user_data: LoginUser, db: Session = Depends(get_db)):
    logged_in = crud_users.login_user(db, user_data.model_dump())
    if logged_in:
        return {"message": "User logged in successfully!"}
    return {"message": "User logging in failed!"}
