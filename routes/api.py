from fastapi import FastAPI
from routes.users import router as user_router
from database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(user_router, prefix='/users', tags=['Users'])