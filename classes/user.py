from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    password_check: str