from pydantic import BaseModel

class Score(BaseModel):
    username: str
    score: int
