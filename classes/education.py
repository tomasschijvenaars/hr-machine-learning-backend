from pydantic import BaseModel

class Education(BaseModel):
    degree: str
    institution: str
    duration: int
