import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class NotificationSetting(Base):
    __tablename__ = "notification_settings"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    daily_reminder = Column(Integer, default=1)
    weekly_report_alert = Column(Integer, default=1)
    updated_at = Column(String, nullable=True)

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    ref_id = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(String, nullable=True)
