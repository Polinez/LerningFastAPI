from datetime import timedelta, datetime
from typing import Optional

from fastapi import FastAPI, HTTPException , status
from Models.Task import Task
from Models.PomodoroSession import PomodoroSession



app = FastAPI()

tasks = [
            {
            "id": 1,
            "title": "Nauka FastAPI",
            "description": "Przygotować przykładowe API z dokumentacją",
            "status": "do wykonania",
            }
        ]

pomodoro_sessions = [
                {
                "task_id": 1,
                "start_time": datetime(2025, 1, 9, 12, 0, 0),
                "end_time": datetime(2025, 1, 9, 12, 25, 0),
                "completed": True,
                }
            ]


def get_task_by_id(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def get_active_pomodoro_for_task(task_id: int):
    for session in pomodoro_sessions:
        if session["task_id"] == task_id and not session["completed"]:
            return session
    return None


@app.get("/")
async def hello_message():
    print("Endpoint '/' został wywołany.")
    return {"message": "Hello, it's my first FastAPI project"}

@app.post("/tasks")
async def create_task(new_task: Task):
    for task in tasks:
        if new_task.title == task["title"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task with this title already exists")

    new_task.id = len(tasks) + 1
    tasks.append({"id": new_task.id, "title": new_task.title, "description": new_task.description, "status": new_task.status})
    return new_task

@app.get("/tasks")
async def get_all_tasks(status: Optional[str] = None):
    if status:
        return [task for task in tasks if task["status"] == status]
    return tasks

@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):
    task = get_task_by_id(task_id)
    if task:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_task: Task):
    task = get_task_by_id(task_id)
    if task:
            task["title"] = updated_task.title
            task["description"] = updated_task.description
            task["status"] = updated_task.status
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    task = get_task_by_id(task_id)
    if task:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@app.post("/pomodoro")
async def create_pomodoro_session(task_id: int,pomodoro_session: PomodoroSession):

    # id exists
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # active session
    if get_active_pomodoro_for_task(task_id):
        raise HTTPException(status_code=400, detail="There is already an active pomodoro session for this task")


    if pomodoro_session.end_time == None:
        pomodoro_session.end_time = pomodoro_session.start_time + timedelta(minutes=25)

    if pomodoro_session.end_time < pomodoro_session.start_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="End time must be greater than start")

    pomodoro_sessions.append({"task_id": task_id, "start_time": pomodoro_session.start_time, "end_time": pomodoro_session.end_time, "completed": pomodoro_session.completed})
    return pomodoro_session

@app.post("/pomodoro/{task_id}/stop")
async def stop_pomodoro_session(task_id: int):
    if not get_task_by_id(task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    active_sesion = get_active_pomodoro_for_task(task_id)
    if not active_sesion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active pomodoro session not found")

    active_sesion["completed"] = True
    return active_sesion

@app.get("/pomodoro/stats")
async def get_pomodoro_stats():
    stats = {}
    total_time = 0

    for session in pomodoro_sessions:
        if session["completed"]:
            stats[session["task_id"]] = stats.get(session["task_id"], 0) + 1
            total_time += (session["end_time"] - session["start_time"]).seconds

    return {"stats": stats, "total_time_minutes": total_time // 60}




