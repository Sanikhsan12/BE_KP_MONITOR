import json
from datetime import datetime
from fastapi import HTTPException
from app.repositories.attendance_repository import AttendanceRepository
from app.models.attendance import Attendance, FaceVector
from app.utils.face_recognition import get_face_vector, compare_faces
from app.core.config import settings
import uuid

class AttendanceService:
    def __init__(self, attendance_repo: AttendanceRepository):
        self.attendance_repo = attendance_repo

    async def register_face(self, mahasiswa_id: str, image_bytes: bytes):
        vector = get_face_vector(image_bytes)
        if not vector:
            raise HTTPException(status_code=400, detail="Wajah tidak terdeteksi dalam gambar")

        vector_json = json.dumps(vector)
        now_str = datetime.now().isoformat()

        existing_vector = await self.attendance_repo.get_face_vector(mahasiswa_id)
        if existing_vector:
            existing_vector.vector = vector_json
            existing_vector.registered_at = now_str
            await self.attendance_repo.update_face_vector(existing_vector)
        else:
            new_vector = FaceVector(
                mahasiswa_id=mahasiswa_id,
                vector=vector_json,
                registered_at=now_str
            )
            await self.attendance_repo.save_face_vector(new_vector)

        await self.attendance_repo.commit()
        return {"mahasiswa_id": mahasiswa_id, "registered_at": now_str, "message": "Wajah berhasil didaftarkan"}

    async def _process_attendance(self, mahasiswa_id: str, image_bytes: bytes, att_type: str):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        timestamp_str = now.isoformat()

        # Cek apakah sudah absen hari ini
        if await self.attendance_repo.check_attendance_exists(mahasiswa_id, att_type, date_str):
            raise HTTPException(status_code=400, detail=f"Sudah melakukan absensi {att_type} pada tanggal {date_str}")

        # Ambil vektor referensi
        known_vector_obj = await self.attendance_repo.get_face_vector(mahasiswa_id)
        if not known_vector_obj:
            raise HTTPException(status_code=400, detail="Wajah belum didaftarkan. Harap registrasi wajah terlebih dahulu.")

        # Ekstrak vektor dari gambar real-time
        unknown_vector = get_face_vector(image_bytes)
        if not unknown_vector:
            raise HTTPException(status_code=400, detail="Wajah tidak terdeteksi dalam gambar yang diunggah")

        # Bandingkan wajah
        is_match = compare_faces(known_vector_obj.vector, unknown_vector, threshold=settings.face_match_threshold)
        if not is_match:
            raise HTTPException(status_code=401, detail="Wajah tidak cocok dengan data yang terdaftar")

        # Buat record absensi
        new_attendance = Attendance(
            id=uuid.uuid4(),
            mahasiswa_id=mahasiswa_id,
            type=att_type,
            timestamp=timestamp_str,
            date=date_str,
            face_verified=True
        )
        
        await self.attendance_repo.save_attendance(new_attendance)
        await self.attendance_repo.commit()
        
        return new_attendance

    async def check_in(self, mahasiswa_id: str, image_bytes: bytes):
        return await self._process_attendance(mahasiswa_id, image_bytes, "datang")

    async def check_out(self, mahasiswa_id: str, image_bytes: bytes):
        return await self._process_attendance(mahasiswa_id, image_bytes, "pulang")

    async def get_attendances(self, mahasiswa_id: str, date: str = None):
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        return await self.attendance_repo.get_attendance_by_date(mahasiswa_id, date)

    async def is_face_registered(self, mahasiswa_id: str) -> bool:
        existing_vector = await self.attendance_repo.get_face_vector(mahasiswa_id)
        return existing_vector is not None
