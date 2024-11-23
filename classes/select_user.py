from pydantic import BaseModel

class SelectUser(BaseModel):
   user_id: int