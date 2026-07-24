import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class DailyReport(Base):
    __tablename__ = "daily_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=True)
    mahasiswa_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    activity = Column(String, nullable=False)
    obstacle = Column(String, nullable=True)
    tomorrow_plan = Column(String, nullable=True)
    report_date = Column(String, nullable=False)
    send_status = Column(String, default="sent")
    submitted_at = Column(String, nullable=True)

class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mahasiswa_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    file_url = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    status = Column(String, default="submitted")
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(String, nullable=True)
    submitted_at = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("mahasiswa_id", "week_number", "year", name="uq_weekly_report"),
    )
