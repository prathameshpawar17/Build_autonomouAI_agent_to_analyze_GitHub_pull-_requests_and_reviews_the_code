from sqlalchemy.orm import Session
from ..db.models import Task
from ..db.models import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_task(task_id: str, db: Session):
    task = Task(task_id=task_id, status="pending")
    db.add(task)
    db.commit()
    return task

def update_task_status(task_id: str, status: str, result: str = None, db: Session = None):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if task:
        task.status = status
        task.result = result
        db.commit()
        return task
    return None

def get_task(task_id: str, db: Session):
    return db.query(Task).filter(Task.task_id == task_id).first()
