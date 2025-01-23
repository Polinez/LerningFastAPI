
from typing import Optional

from fastapi import FastAPI

from Database.database import create_db_and_tables, DB_handlerDependency
from Models.Task import Task
from Models.PomodoroSession import PomodoroSession



app = FastAPI()

@app.get("/")
async def hello_message():
    create_db_and_tables()
    return {"message": "Hello, it's my first FastAPI project"}

@app.post("/tasks")
async def create_task(new_task: Task, handler: DB_handlerDependency ):
    return handler.add_task(new_task)

@app.get("/tasks")
async def get_all_tasks(handler: DB_handlerDependency, task_status: Optional[str] = None ):
    return handler.get_all_tasks(task_status)


@app.get("/tasks/{task_id}")
async def get_task(task_id: int, handler: DB_handlerDependency):
    return handler.get_task_by_id(task_id)


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_task: Task, handler: DB_handlerDependency):
    return handler.update_task(task_id, updated_task)


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, handler: DB_handlerDependency):
    return handler.delete_task(task_id)



@app.post("/pomodoro")
async def create_pomodoro_session(task_id: int,pomodoro_session: PomodoroSession, handler: DB_handlerDependency):
    return handler.add_pomodoro_session(task_id, pomodoro_session)


@app.post("/pomodoro/{task_id}/stop")
async def stop_pomodoro_session(task_id: int, handler: DB_handlerDependency):
    return handler.stop_pomodoro_session(task_id)


@app.get("/pomodoro/stats")
async def get_pomodoro_stats(handler: DB_handlerDependency):
    return handler.get_pomodoro_stats()





