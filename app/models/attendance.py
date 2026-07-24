import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mahasiswa_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(10), nullable=False)
    timestamp = Column(Text, nullable=False)
    date = Column(Text, nullable=False)
    face_verified = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint("mahasiswa_id", "type", "date", name="uq_attendance_per_day"),
    )

class FaceVector(Base):
    __tablename__ = "face_vectors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mahasiswa_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    vector = Column(Text, nullable=False)
    registered_at = Column(Text, nullable=False)
