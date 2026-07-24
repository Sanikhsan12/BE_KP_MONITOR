import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mahasiswa_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="todo")
    task_date = Column(String, nullable=False)
    is_verified = Column(Integer, default=0)
    is_deleted = Column(Integer, default=0)
    created_at = Column(String, nullable=True)
    updated_at = Column(String, nullable=True)

class TaskPhoto(Base):
    __tablename__ = "task_photos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    photo_url = Column(String, nullable=False)
    uploaded_at = Column(String, nullable=True)

class TaskProgressNote(Base):
    __tablename__ = "task_progress_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    note = Column(String, nullable=False)
    created_at = Column(String, nullable=True)
