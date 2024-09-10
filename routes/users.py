from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import crud.users as crud_users
from database import get_db
from schemas import LoginUser, RegisterUser

router = APIRouter()


@router.post("/register")
def register_user(user_data: RegisterUser, db: Session = Depends(get_db)):
    crud_users.register_user(db, user_data.model_dump())
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"detail": "User created successfully!"},
    )


@router.post("/login")
def login_user(user_data: LoginUser, db: Session = Depends(get_db)):
    return crud_users.login_user(db, user_data.model_dump())
