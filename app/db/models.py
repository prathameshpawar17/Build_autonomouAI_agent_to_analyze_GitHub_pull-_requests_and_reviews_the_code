from sqlalchemy import Column, String, Text, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import settings

Base = declarative_base()
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Task(Base):
    __tablename__ = "tasks"
    task_id = Column(String, primary_key=True, index=True)
    status = Column(Enum("pending", "processing", "completed", "failed", name="status_enum"), default="pending")
    result = Column(Text, nullable=True)
