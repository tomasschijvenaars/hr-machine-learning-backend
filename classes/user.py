from pydantic import BaseModel

class RegisterUser(BaseModel):
    username: str
    password: str
    password_check: str

class LoginUser(BaseModel):
    username: str
    password: str
