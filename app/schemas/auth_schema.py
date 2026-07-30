from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequestBase(BaseModel):
    role: str
    name: str
    email: EmailStr
    password: str

class RegisterMahasiswaRequest(RegisterRequestBase):
    nim: str
    universitas: str
    divisi: str
    periode_mulai: str
    periode_selesai: str

class RegisterMentorRequest(RegisterRequestBase):
    nik: str
    divisi: str
    jabatan: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str

class LoginResponseData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class LoginResponse(BaseModel):
    status: str = "success"
    data: LoginResponseData
