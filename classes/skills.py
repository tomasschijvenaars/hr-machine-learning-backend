from pydantic import BaseModel

class Skills(BaseModel):
    programming_languages: list[str]
    frameworks_and_tools: list[str]
    soft_skills: list[str]
