from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.attendance import Attendance, FaceVector
from typing import Optional, List

class AttendanceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_face_vector(self, mahasiswa_id: str) -> Optional[FaceVector]:
        result = await self.session.execute(
            select(FaceVector).where(FaceVector.mahasiswa_id == mahasiswa_id)
        )
        return result.scalars().first()

    async def save_face_vector(self, face_vector: FaceVector):
        self.session.add(face_vector)

    async def update_face_vector(self, face_vector: FaceVector):
        self.session.add(face_vector)

    async def save_attendance(self, attendance: Attendance):
        self.session.add(attendance)

    async def get_attendance_by_date(self, mahasiswa_id: str, date: str) -> List[Attendance]:
        result = await self.session.execute(
            select(Attendance).where(
                Attendance.mahasiswa_id == mahasiswa_id,
                Attendance.date == date
            )
        )
        return result.scalars().all()

    async def check_attendance_exists(self, mahasiswa_id: str, att_type: str, date: str) -> bool:
        result = await self.session.execute(
            select(Attendance).where(
                Attendance.mahasiswa_id == mahasiswa_id,
                Attendance.type == att_type,
                Attendance.date == date
            )
        )
        return result.scalars().first() is not None

    async def commit(self):
        await self.session.commit()
