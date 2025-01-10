from pydantic import BaseModel


class Task(BaseModel):
    id = 0
    def __init__(self, title: str, description: str, status: str):
        self.title = title
        self.description = description
        self.status = status
        Task.id += 1