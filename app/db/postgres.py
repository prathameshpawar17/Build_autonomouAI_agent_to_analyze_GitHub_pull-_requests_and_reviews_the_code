from sqlalchemy.orm import Session
from .models import Task, SessionLocal
from ..logger import logging

# Dependency to provide a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new task
def create_task(task_id: str, db: Session):
    try:
        task = Task(task_id=task_id, status="pending")
        db.add(task)
        db.commit()
        db.refresh(task)  # Ensure the task reflects its committed state
        logging.info(f"Task created with ID: {task_id}")
        return task
    except Exception as e:
        db.rollback()  # Rollback in case of error
        logging.error(f"Error creating task: {e}")
        raise

# Update task status
def update_task_status(task_id: str, status: str, result: str = None, db: Session = None):
    try:
        task = db.query(Task).filter(Task.task_id == task_id).first()
        if not task:
            logging.warning(f"Task with ID {task_id} not found.")
            return None

        task.status = status
        task.result = result
        db.commit()
        db.refresh(task)
        logging.info(f"Task with ID {task_id} updated to status: {status}")
        return task
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating task status: {e}")
        raise

# Retrieve a task by ID
def get_task(task_id: str, db: Session):
    try:
        task = db.query(Task).filter(Task.task_id == task_id).first()
        if task:
            logging.info(f"Task retrieved with ID: {task_id}")
        else:
            logging.warning(f"Task with ID {task_id} not found.")
        return task
    except Exception as e:
        logging.error(f"Error retrieving task with ID {task_id}: {e}")
        raise
