from pydantic import BaseModel
from typing import Optional, List

class TaskCreateRequest(BaseModel):
    title: str
    description: str
    status: str
    task_date: Optional[str] = None # Jika kosong bisa diisi otomatis di service dengan hari ini

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    task_date: Optional[str] = None

class TaskPhotoSchema(BaseModel):
    id: str
    photo_url: str
    uploaded_at: Optional[str] = None

class TaskProgressNoteSchema(BaseModel):
    id: str
    note: str
    created_at: Optional[str] = None

class TaskResponse(BaseModel):
    id: str
    mahasiswa_id: str
    title: str
    description: str
    status: str
    task_date: str
    is_verified: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    photos: List[TaskPhotoSchema] = []
    notes: List[TaskProgressNoteSchema] = []

class TaskProgressNoteCreate(BaseModel):
    note: str
