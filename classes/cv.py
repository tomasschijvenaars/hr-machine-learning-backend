from pydantic import BaseModel

# Models
from  classes.education import Education
from classes.skills import Skills

class Cv(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    linkedin: str
    github: str
    education: Education
    work_experience_total_years: str
    skills: Skills