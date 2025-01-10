from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PomodoroSession(BaseModel):
    task_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    completed: bool