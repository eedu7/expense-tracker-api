
from pydantic import BaseModel, EmailStr,Field


class User(BaseModel):
    email: EmailStr
    password: str


class RegisterUser(User):
    username: str


class LoginUser(User):
    pass

class CurrentUser(BaseModel):
    id: int = Field(None, description="User ID")

    class Config:
        validate_assignment = True