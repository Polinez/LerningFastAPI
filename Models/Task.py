from enum import Enum

from sqlmodel import SQLModel, Field
from typing import Optional

class Status(str, Enum):
    do_wykonania = "do wykonania"
    w_trakcie = "w trakcie"
    zakonczone = "zakończone"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    status: Status = Field(default=Status.do_wykonania)