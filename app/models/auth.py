import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class AuthSession(Base):
    __tablename__ = "auth_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, nullable=False)
    device_info = Column(String, nullable=True)
    expires_at = Column(String, nullable=False)
    created_at = Column(String, nullable=True)
    revoked_at = Column(String, nullable=True)

class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, nullable=False)
    expires_at = Column(String, nullable=False)
    used_at = Column(String, nullable=True)
    created_at = Column(String, nullable=True)
