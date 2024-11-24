from pydantic import BaseModel

class AddData(BaseModel):
    percent_skills: int
    percent_experience: int
    job_succesful: int
