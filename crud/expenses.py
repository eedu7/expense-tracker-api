from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from models import Expense


def get_all_expense(db: Session):
    try:
        return db.query(Expense).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exception on fetching expenses data",
        )


def get_by_id(db: Session, expense_id: int) -> Expense:
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Expense with ID {expense_id} does not exist",
            )
        return expense
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exception on fetching expenses: ({e})",
        )


def get_expense_by_date_range(db: Session, start_date, end_date, user_id):
    try:
        expenses = (
            db.query(Expense)
            .filter(
                and_(
                    Expense.date >= start_date,
                    Expense.date <= end_date,
                    Expense.user_id == user_id,
                )
            )
            .all()
        )
        if not expenses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No expenses found between {start_date} and {end_date}",
            )

        return expenses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exception on fetching expenses by date range: ({e})",
        )


def get_by_user_id(db: Session, user_id: int) -> Expense:
    try:
        expense = db.query(Expense).filter(Expense.user_id == user_id).all()
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Expense for the User ID {user_id} does not exist",
            )
        return expense
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exception on fetching expense: ({e})",
        )


def add_expense(db: Session, expense_data: dict, user_id: int) -> Expense:
    expense_data["user_id"] = user_id
    try:
        expense = Expense(**expense_data)
        db.add(expense)
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exception on adding expense: ({e})",
        )


def remove_expense(db: Session, expense_id: int, user_id: int) -> bool:
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} does not exist",
        )

    if expense.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User ID {user_id} is not the owner of the Expense",
        )
    db.delete(expense)
    db.commit()
    return True


def update_expense(
    db: Session, expense_id: int, expense_data: dict, user_id: int
) -> bool:
    expense = get_by_id(db, expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} does not exist",
        )
    if expense.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User ID {user_id} is not the owner of the Expense",
        )

    for key, value in expense_data.items():
        setattr(expense, key, value)

    db.commit()

    return True
