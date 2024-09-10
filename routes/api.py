from fastapi import FastAPI

from database import Base, engine
from routes.users import router as user_router
from .expenses import router as expense_router
Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(expense_router, prefix="/expenses", tags=["Expenses"])