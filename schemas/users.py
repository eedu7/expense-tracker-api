from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    password: str


class RegisterUser(User):
    email: EmailStr


class LoginUser(BaseModel):
    pass
