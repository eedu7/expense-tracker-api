from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import crud.expenses as crud_expenses
from database import get_db
from schemas import CreateExpense, ResponseExpense, UpdateExpense

router = APIRouter()


@router.get("/")
def get_expenses(db: Session = Depends(get_db)) -> List[ResponseExpense]:
    return crud_expenses.get_all_expense(db)


@router.post("/{user_id}")
def create_expense(
    user_id: int, expense_data: CreateExpense, db: Session = Depends(get_db)
):
    crud_expenses.add_expense(
        db, expense_data.model_dump(exclude_none=True), user_id=user_id
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        "detail": "Expense added successfully"
    })



@router.get("/{expense_id}")
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    return crud_expenses.get_by_id(db, expense_id)


@router.put("/{expense_id}/{user_id}")
def update_expense(
    expense_id: int,
    user_id: int,
    expense_data: UpdateExpense,
    db: Session = Depends(get_db),
):
    crud_expenses.update_expense(
        db, expense_id, expense_data.model_dump(exclude_none=True), user_id=user_id
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": f"Expense with ID ({expense_id}) has been updated."},
    )


@router.delete("/{expense_id}/{user_id}")
def delete_expense(expense_id: int, user_id: int, db: Session = Depends(get_db)):
    crud_expenses.remove_expense(db, user_id=user_id, expense_id=expense_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": f"Expense with ID ({expense_id}) has been deleted."},
    )
