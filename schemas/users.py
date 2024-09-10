from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str


class RegisterUser(User):
    username: str


class LoginUser(User):
    pass
