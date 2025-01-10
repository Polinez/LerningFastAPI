from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

class PomodoroSession(BaseModel):
    task_id: int
    start_time: datetime = Field(default_factory=lambda: datetime.now())
    end_time: Optional[datetime] = None
    completed: bool = False