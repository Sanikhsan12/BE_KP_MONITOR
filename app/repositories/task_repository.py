from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, and_, desc
from app.models.task import Task, TaskPhoto, TaskProgressNote
from typing import Optional, List

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task: Task):
        self.session.add(task)

    async def update_task(self, task: Task):
        self.session.add(task)

    async def get_task_by_id(self, task_id: str, mahasiswa_id: str) -> Optional[Task]:
        result = await self.session.execute(
            select(Task).where(Task.id == task_id, Task.mahasiswa_id == mahasiswa_id, Task.is_deleted == 0)
        )
        return result.scalars().first()

    async def get_tasks(self, mahasiswa_id: str, status: str, start_date: str, end_date: str) -> List[Task]:
        query = select(Task).where(Task.mahasiswa_id == mahasiswa_id, Task.is_deleted == 0)
        
        if status and status.lower() != "all":
            query = query.where(Task.status == status)
            
        if start_date and end_date:
            query = query.where(Task.task_date >= start_date, Task.task_date <= end_date)
            
        query = query.order_by(desc(Task.task_date), desc(Task.created_at))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add_task_photo(self, photo: TaskPhoto):
        self.session.add(photo)

    async def get_task_photos(self, task_id: str) -> List[TaskPhoto]:
        result = await self.session.execute(select(TaskPhoto).where(TaskPhoto.task_id == task_id))
        return result.scalars().all()

    async def add_task_progress_note(self, note: TaskProgressNote):
        self.session.add(note)

    async def get_task_progress_notes(self, task_id: str) -> List[TaskProgressNote]:
        result = await self.session.execute(
            select(TaskProgressNote).where(TaskProgressNote.task_id == task_id).order_by(desc(TaskProgressNote.created_at))
        )
        return result.scalars().all()

    async def commit(self):
        await self.session.commit()
