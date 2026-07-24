from fastapi import APIRouter, Depends, File, UploadFile, Query, HTTPException, Body, Form
from typing import List, Optional
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.core.dependencies import get_current_user, get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task_schema import TaskCreateRequest, TaskUpdateRequest, TaskResponse, TaskProgressNoteCreate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_task_service(db: AsyncSession = Depends(get_db_session)):
    repo = TaskRepository(db)
    return TaskService(repo)

def require_mahasiswa(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "mahasiswa":
        raise HTTPException(status_code=403, detail="Hanya mahasiswa yang dapat mengakses endpoint ini")
    return current_user

@router.get("", response_model=dict, responses={
    200: {"description": "Berhasil mendapatkan daftar tugas"}
})
async def get_tasks(
    status: str = Query("all", description="Filter status: all, done, todo, inprogress"),
    date_filter: Optional[str] = Query(None, description="Rentang tanggal H-3 sampai H+3, opsional"),
    current_user=Depends(require_mahasiswa),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Mendapatkan daftar tugas harian milik mahasiswa.
    Filter status dan tanggal H-3 s.d. H+3.
    """
    tasks = await task_service.get_tasks(current_user["sub"], status, date_filter)
    # Konversi ke dict karena model dict yang diharapkan di respons
    return {"status": "success", "data": [t.dict() for t in tasks]}

@router.post("", response_model=dict, responses={201: {"description": "Berhasil membuat tugas"}})
async def create_task(
    title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    task_date: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user=Depends(require_mahasiswa),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Membuat tugas baru.
    Mendukung upload foto (opsional) menggunakan form-data.
    """
    req = TaskCreateRequest(title=title, description=description, status=status, task_date=task_date)
    result = await task_service.create_task(current_user["sub"], req, file)
    return {"status": "success", "data": result}

@router.put("/{task_id}", response_model=dict)
async def update_task(
    task_id: str,
    req: TaskUpdateRequest = Body(...),
    current_user=Depends(require_mahasiswa),
    task_service: TaskService = Depends(get_task_service)
):
    """Memperbarui informasi tugas (Judul, deskripsi, status, dll)."""
    result = await task_service.update_task(current_user["sub"], task_id, req)
    return {"status": "success", "data": result}

@router.delete("/{task_id}", response_model=dict)
async def delete_task(
    task_id: str,
    current_user=Depends(require_mahasiswa),
    task_service: TaskService = Depends(get_task_service)
):
    """Menghapus tugas harian (soft delete)."""
    result = await task_service.delete_task(current_user["sub"], task_id)
    return {"status": "success", "data": result}

@router.post("/{task_id}/progress", response_model=dict)
async def add_progress_note(
    task_id: str,
    req: TaskProgressNoteCreate = Body(...),
    current_user=Depends(require_mahasiswa),
    task_service: TaskService = Depends(get_task_service)
):
    """Menambahkan catatan progres (progress note) ke tugas harian tertentu."""
    result = await task_service.add_progress_note(current_user["sub"], task_id, req.note)
    return {"status": "success", "data": result}

@router.post("/{task_id}/photos", response_model=dict)
async def add_task_photo(
    task_id: str,
    file: UploadFile = File(...),
    current_user=Depends(require_mahasiswa),
    task_service: TaskService = Depends(get_task_service)
):
    """Menambahkan lampiran foto ke tugas harian."""
    result = await task_service.add_task_photo(current_user["sub"], task_id, file)
    return {"status": "success", "data": result}
