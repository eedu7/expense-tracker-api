from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import crud.expenses as crud_expenses
from database import get_db
from dependencies import AuthenticationRequired
from schemas import CreateExpense, ResponseExpense, UpdateExpense

router = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get("/")
def get_all_expenses(
    request: Request,
    past_week: bool | None = None,
    past_month: bool | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
):
    if past_week:
        end_date = datetime.now()
        print("Past Week")
        start_date = end_date - timedelta(days=7)
        return crud_expenses.get_expense_by_date_range(
            db, start_date, end_date, request.user.id
        )
    elif past_month:
        print("Past Month")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        return crud_expenses.get_expense_by_date_range(
            db, start_date, end_date, request.user.id
        )
    elif start_date and end_date:
        print("Start Date -> End Date")
        return crud_expenses.get_expense_by_date_range(
            db, start_date, end_date, request.user.id
        )
    else:
        print("Else")
        return crud_expenses.get_by_user_id(db, request.user.id)


@router.post("/")
def create_expense(
    request: Request, expense_data: CreateExpense, db: Session = Depends(get_db)
):
    user_id = request.user.id
    crud_expenses.add_expense(
        db, expense_data.model_dump(exclude_none=True), user_id=user_id
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"detail": "Expense added successfully"},
    )


@router.get("/{expense_id}")
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    return crud_expenses.get_by_id(db, expense_id)


@router.put("/{expense_id}")
def update_expense(
    expense_id: int,
    request: Request,
    expense_data: UpdateExpense,
    db: Session = Depends(get_db),
):
    user_id = request.user.id
    crud_expenses.update_expense(
        db, expense_id, expense_data.model_dump(exclude_none=True), user_id=user_id
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": f"Expense with ID ({expense_id}) has been updated."},
    )


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.user.id
    crud_expenses.remove_expense(db, user_id=user_id, expense_id=expense_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": f"Expense with ID ({expense_id}) has been deleted."},
    )
