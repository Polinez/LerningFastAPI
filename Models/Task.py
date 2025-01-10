from typing import Optional
from pydantic import BaseModel,Field


class Task(BaseModel):
    id : int
    title : str = Field(..., min_length=3, max_length=100)
    description : Optional[str] = Field(None, max_length=300)
    status : str = Field("do wykonania", pattern="^(do wykonania|w trakcie|zakończone)$")