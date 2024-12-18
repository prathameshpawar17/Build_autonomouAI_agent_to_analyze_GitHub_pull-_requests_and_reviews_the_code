from sqlalchemy import Column, String, Text, Enum, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import Config
from ..logger import logging

# Base class for models
Base = declarative_base()

# Database engine and session factory
DATABASE_URL = Config.DATABASE_URL
engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` for SQL query logging
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Task model
class Task(Base):
    __tablename__ = "Github_table"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(String(255), nullable=False)
    status = Column(String(50), Enum("pending", "processing", "completed", "failed", name="status_enum"), default="pending")
    result = Column(Text, nullable=True)

# Table creation function
def create_tables():
    try:
        logging.info("Creating tables (if not already present)...")
        Base.metadata.create_all(bind=engine)
        logging.info("Tables created successfully.")
    except Exception as e:
        logging.error(f"Error while creating tables: {e}")
        raise

# Ensure tables are created when this module is imported
create_tables()
