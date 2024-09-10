from sqlalchemy import Date, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from extras import ExpenseCategory


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(Float, nullable=True)
    category: Mapped[ExpenseCategory] = mapped_column(
        Enum(ExpenseCategory), nullable=True
    )
    description: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[str] = mapped_column(Date, nullable=True)
    user_id: Mapped[Integer] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
