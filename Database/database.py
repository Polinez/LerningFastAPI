import os
from datetime import  timedelta
from fastapi import Depends, HTTPException, status
from typing import Annotated, Optional
from sqlmodel import create_engine, Session, SQLModel, select

from Models.Task import Task
from Models.PomodoroSession import PomodoroSession

# DATABASE_URL = "sqlite:///Database/database.db"
#
# engine = create_engine(DATABASE_URL, echo=True)


# database configuration
if os.getenv("ENVIRONMENT") == "development":
    DATABASE_URL = "sqlite:///./database.db"
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# creating an dependency for a session to dont create it every time
sesionDependency = Annotated[Session, Depends(get_session)]


class DBStorageHandler:
    """
    Handler for database operations
    """
    def __init__(self,session: Session):
        self.session = session

    def add_task(self, task: Task) -> Task:
        """
        Add task to database
        """
        existing_task = self.session.exec(select(Task).where(Task.title == task.title)).first()
        if existing_task:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Task with this title already exists"
            )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_all_tasks(self, status: Optional[str] = None) -> list[Task]:
        """
        Get all tasks from database
        """
        if status:
            tasks = self.session.exec(select(Task).where(Task.status == status)).all()
        else:
            tasks = self.session.exec(select(Task)).all()
        return tasks

    def get_task_by_id(self,task_id: int) -> Task:
        """
        Get task by id from database
        """
        task = self.session.exec(select(Task).where(Task.id == task_id)).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task

    def update_task(self, task_id: int, updated_task: Task) -> Task:
        """
        Update task in database
        """
        task = self.get_task_by_id(task_id)
        task.title = updated_task.title
        task.description = updated_task.description
        task.status = updated_task.status
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: int) -> None:
        """
        Delete task from database
        """
        task = self.get_task_by_id(task_id)
        self.session.delete(task)
        self.session.commit()


#TODO: repair formating datetme
    def add_pomodoro_session(self, task_id: int, pomodoro_session: PomodoroSession) -> PomodoroSession:
        """
        Add a new Pomodoro session to the database.
        """
        # Check if there is an active session for this task
        active_session = self.session.exec(select(PomodoroSession).where(PomodoroSession.task_id == task_id, PomodoroSession.completed == False)).first()
        if active_session:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is already an active Pomodoro session for this task")

        # Set end_time if not provided
        if pomodoro_session.end_time is None:
            pomodoro_session.end_time = pomodoro_session.start_time + timedelta(minutes=25)

        # Validate end_time
        if pomodoro_session.end_time < pomodoro_session.start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be greater than start time"
            )

        pomodoro_session.task_id = task_id
        self.session.add(pomodoro_session)
        self.session.commit()
        self.session.refresh(pomodoro_session)
        return pomodoro_session

    def stop_pomodoro_session(self, task_id: int) -> PomodoroSession:
        """
        Stop the Pomodoro session for the given task.
        """
        task = self.session.get(Task, task_id)
        active_session = self.session.exec(
            select(PomodoroSession).where(PomodoroSession.task_id == task_id, PomodoroSession.completed == False)).first()
        if not active_session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active Pomodoro session for this task")

        active_session.completed = True
        self.session.commit()
        self.session.refresh(active_session)
        return active_session

    def get_pomodoro_stats(self):
        """
        Get statistics for completed Pomodoro sessions.
        """
        stats = {}
        total_time = 0

        completed_sessions = self.session.exec(select(PomodoroSession).where(PomodoroSession.completed == True)).all()

        for session in completed_sessions:
            stats[session.task_id] = stats.get(session.task_id, 0) + 1
            total_time += (session.end_time - session.start_time).seconds

        return {"stats": stats, "total_time_minutes": total_time // 60}


# Dependency for DBStorageHandler to dont wite it every time
def get_DB_handler(session: Session = Depends(get_session)) -> DBStorageHandler:
    return DBStorageHandler(session)
DB_handlerDependency = Annotated[DBStorageHandler, Depends(get_DB_handler)]