# FastAPI Pomodoro and Task Management API
This project was created during my university class, where I learned FastAPI.
This project is a FastAPI-based application for managing tasks and tracking Pomodoro sessions.

## Features
1. Task Management:

- Create a new task
- Retrieve all tasks or filter by status
- Retrieve a task by ID
- Update a task
- Delete a task
- Pomodoro Session Management:

2. Create a Pomodoro session for a specific task
- Stop an active Pomodoro session
- View Pomodoro statistics, including the number of sessions and total time spent on tasks
  
## Installation

- Install dependencies:
```bash
pip install -r requirements.txt
```
- Run the application:
```
fastapi dev main.py
```
or
```
uvicorn main:app --reload
```
