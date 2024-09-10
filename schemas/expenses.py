from datetime import date
from typing import Union

from pydantic import BaseModel, Field, field_validator

from extras import ExpenseCategory


class CreateExpense(BaseModel):
    category: ExpenseCategory = Field(..., examples=[ExpenseCategory.FOOD])
    description: str = Field(..., examples=["Lunch at cafe"])
    amount: float = Field(
        ...,
        examples=[50.0],
    )
    date: date

    @field_validator("amount")
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError("Amount cannot be negative")
        return v


class UpdateExpense(BaseModel):
    category: ExpenseCategory | None = Field(None, examples=[ExpenseCategory.FOOD])
    description: str | None = Field(None, examples=["Lunch at cafe"])
    amount: float | None = Field(
        None,
        examples=[50.0],
    )
    date: date = None

    @field_validator("amount")
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError("Amount cannot be negative")
        return v


class ResponseExpense(BaseModel):
    id: int = Field(..., examples=[0])
    category: ExpenseCategory | None = Field(None, examples=[ExpenseCategory.FOOD])
    description: str | None = Field(None, examples=["Lunch at cafe"])
    amount: float | None = Field(
        None,
        examples=[50.0],
    )
    date: date
