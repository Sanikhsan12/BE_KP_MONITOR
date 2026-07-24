from pydantic import BaseModel
from typing import Optional

class MahasiswaProfileSchema(BaseModel):
    nim: str
    universitas: str
    divisi: str
    mentor_id: Optional[str] = None
    periode_mulai: str
    periode_selesai: str

class MentorProfileSchema(BaseModel):
    nik: str
    divisi: str
    jabatan: str

class UserProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    avatar_url: Optional[str] = None
    mahasiswa_profile: Optional[MahasiswaProfileSchema] = None
    mentor_profile: Optional[MentorProfileSchema] = None

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    divisi: Optional[str] = None
    universitas: Optional[str] = None
    jabatan: Optional[str] = None
