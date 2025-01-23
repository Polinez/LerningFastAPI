from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional



class PomodoroSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    completed: bool = Field(default=False)
