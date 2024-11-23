from pydantic import BaseModel

class User(BaseModel):
    name: str
    skills: str
    experience: str
    goodEnough: str

