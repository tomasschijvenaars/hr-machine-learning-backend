from pydantic import BaseModel

class Job(BaseModel):
    name: str
    function: str
    years_of_experience: int
    skills: list[str]
    year_salary: int