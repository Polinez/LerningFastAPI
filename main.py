from fastapi import FastAPI
from Task import Task

app = FastAPI()

tasksList = {}

@app.post("/task")
def create_task(title: str, description: str, status: str):
    task = Task(title, description, status)
    if task.id in tasksList.keys():
        return {"message": "Task already exists"}
    tasksList[task.id] = task
    return {"message": "Task created successfully"}
