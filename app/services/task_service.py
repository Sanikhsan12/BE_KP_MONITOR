from fastapi import HTTPException
from app.repositories.task_repository import TaskRepository
from app.schemas.task_schema import TaskCreateRequest, TaskUpdateRequest, TaskResponse, TaskPhotoSchema, TaskProgressNoteSchema
from app.models.task import Task, TaskPhoto, TaskProgressNote
from app.utils.file_upload import save_upload_file
from datetime import datetime, timedelta
import uuid

class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    async def get_tasks(self, mahasiswa_id: str, status: str = "all", date_filter: str = None) -> list:
        # Default date filter: H-3 to H+3 if no specific logic
        # For simplicity, if date_filter is not provided, we calculate H-3 and H+3
        today = datetime.now()
        start_date_str = (today - timedelta(days=3)).strftime("%Y-%m-%d")
        end_date_str = (today + timedelta(days=3)).strftime("%Y-%m-%d")

        tasks = await self.task_repo.get_tasks(mahasiswa_id, status, start_date_str, end_date_str)
        result = []
        for t in tasks:
            photos = await self.task_repo.get_task_photos(t.id)
            notes = await self.task_repo.get_task_progress_notes(t.id)
            
            photo_schemas = [TaskPhotoSchema(id=str(p.id), photo_url=p.photo_url, uploaded_at=p.uploaded_at) for p in photos]
            note_schemas = [TaskProgressNoteSchema(id=str(n.id), note=n.note, created_at=n.created_at) for n in notes]
            
            result.append(TaskResponse(
                id=str(t.id),
                mahasiswa_id=str(t.mahasiswa_id),
                title=t.title,
                description=t.description,
                status=t.status,
                task_date=t.task_date,
                is_verified=t.is_verified,
                created_at=t.created_at,
                updated_at=t.updated_at,
                photos=photo_schemas,
                notes=note_schemas
            ))
        return result

    async def create_task(self, mahasiswa_id: str, req: TaskCreateRequest, file = None) -> dict:
        now_str = datetime.now().isoformat()
        task_id = uuid.uuid4()
        
        t_date = req.task_date if req.task_date else datetime.now().strftime("%Y-%m-%d")

        new_task = Task(
            id=task_id,
            mahasiswa_id=mahasiswa_id,
            title=req.title,
            description=req.description,
            status=req.status,
            task_date=t_date,
            is_verified=0,
            is_deleted=0,
            created_at=now_str,
            updated_at=now_str
        )
        await self.task_repo.create_task(new_task)
        
        if file:
            photo_url = save_upload_file(file, subfolder="tasks")
            new_photo = TaskPhoto(
                id=uuid.uuid4(),
                task_id=task_id,
                photo_url=photo_url,
                uploaded_at=now_str
            )
            await self.task_repo.add_task_photo(new_photo)

        await self.task_repo.commit()
        
        return TaskResponse(
            id=str(task_id),
            mahasiswa_id=str(new_task.mahasiswa_id),
            title=new_task.title,
            description=new_task.description,
            status=new_task.status,
            task_date=new_task.task_date,
            is_verified=new_task.is_verified,
            created_at=new_task.created_at,
            updated_at=new_task.updated_at,
            photos=[TaskPhotoSchema(id=str(new_photo.id), photo_url=new_photo.photo_url, uploaded_at=new_photo.uploaded_at)] if file else [],
            notes=[]
        ).dict()

    async def update_task(self, mahasiswa_id: str, task_id: str, req: TaskUpdateRequest) -> dict:
        task = await self.task_repo.get_task_by_id(task_id, mahasiswa_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tugas tidak ditemukan")

        if req.title: task.title = req.title
        if req.description: task.description = req.description
        if req.status: task.status = req.status
        if req.task_date: task.task_date = req.task_date
        
        task.updated_at = datetime.now().isoformat()
        await self.task_repo.update_task(task)
        await self.task_repo.commit()
        
        photos = await self.task_repo.get_task_photos(task.id)
        notes = await self.task_repo.get_task_progress_notes(task.id)
        photo_schemas = [TaskPhotoSchema(id=str(p.id), photo_url=p.photo_url, uploaded_at=p.uploaded_at) for p in photos]
        note_schemas = [TaskProgressNoteSchema(id=str(n.id), note=n.note, created_at=n.created_at) for n in notes]

        return TaskResponse(
            id=str(task.id),
            mahasiswa_id=str(task.mahasiswa_id),
            title=task.title,
            description=task.description,
            status=task.status,
            task_date=task.task_date,
            is_verified=task.is_verified,
            created_at=task.created_at,
            updated_at=task.updated_at,
            photos=photo_schemas,
            notes=note_schemas
        ).dict()

    async def add_progress_note(self, mahasiswa_id: str, task_id: str, note: str) -> dict:
        task = await self.task_repo.get_task_by_id(task_id, mahasiswa_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tugas tidak ditemukan")
            
        new_note = TaskProgressNote(
            id=uuid.uuid4(),
            task_id=task.id,
            note=note,
            created_at=datetime.now().isoformat()
        )
        await self.task_repo.add_task_progress_note(new_note)
        await self.task_repo.commit()
        return {"id": str(new_note.id), "message": "Catatan progres berhasil ditambahkan"}

    async def add_task_photo(self, mahasiswa_id: str, task_id: str, file) -> dict:
        task = await self.task_repo.get_task_by_id(task_id, mahasiswa_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tugas tidak ditemukan")
            
        photo_url = save_upload_file(file, subfolder="tasks")
        new_photo = TaskPhoto(
            id=uuid.uuid4(),
            task_id=task.id,
            photo_url=photo_url,
            uploaded_at=datetime.now().isoformat()
        )
        await self.task_repo.add_task_photo(new_photo)
        await self.task_repo.commit()
        return {"id": str(new_photo.id), "url": photo_url, "message": "Foto berhasil diunggah"}

    async def delete_task(self, mahasiswa_id: str, task_id: str) -> dict:
        task = await self.task_repo.get_task_by_id(task_id, mahasiswa_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tugas tidak ditemukan")
            
        task.is_deleted = 1
        await self.task_repo.update_task(task)
        await self.task_repo.commit()
        return {"message": "Tugas berhasil dihapus"}
