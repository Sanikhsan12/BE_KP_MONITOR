from pydantic import BaseModel
from typing import Optional

class AttendanceResponse(BaseModel):
    id: str
    mahasiswa_id: str
    type: str
    timestamp: str
    date: str
    face_verified: bool

class RegisterFaceResponse(BaseModel):
    mahasiswa_id: str
    registered_at: str
    message: str
