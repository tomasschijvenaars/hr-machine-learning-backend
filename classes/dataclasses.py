from pydantic import BaseModel

class Education(BaseModel):
    degree: str
    institution: str
    duration: str

class Skills(BaseModel):
    programming_languages: list[str]
    frameworks_and_tools: list[str]
    soft_skills: list[str]

class EmployeeCV(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    linkedin: str
    github: str
    education: Education
    work_experience_total_years: str
    skills: Skills