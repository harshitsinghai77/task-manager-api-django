from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Enum
from database import Base, engine
from datetime import datetime
import enum

class UserTaskStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"

class UserTask(Base):
    __tablename__ = 'user_tasks'

    task_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=True)
    status = Column(Enum(UserTaskStatus), default=UserTaskStatus.pending, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class DeadLetteredTask(Base):
    __tablename__ = "dead_letter_queue_tasks"

    celery_task_id = Column(String(36), primary_key=True)
    args = Column(Text)
    kwargs = Column(Text)
    error = Column(Text)
    failed_at = Column(DateTime, default=datetime.utcnow)
