import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    is_active = Column(Integer, default=1)
    created_at = Column(String, nullable=True)
    updated_at = Column(String, nullable=True)

class MahasiswaProfile(Base):
    __tablename__ = "mahasiswa_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    nim = Column(String, unique=True, nullable=False)
    universitas = Column(String, nullable=False)
    divisi = Column(String, nullable=False)
    mentor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    periode_mulai = Column(String, nullable=False)
    periode_selesai = Column(String, nullable=False)

class MentorProfile(Base):
    __tablename__ = "mentor_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    nik = Column(String, unique=True, nullable=False)
    divisi = Column(String, nullable=False)
    jabatan = Column(String, nullable=False)
