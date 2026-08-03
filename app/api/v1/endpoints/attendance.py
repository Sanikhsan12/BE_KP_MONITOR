from fastapi import APIRouter, Depends, File, UploadFile, Query, HTTPException
from typing import List, Optional
from app.services.attendance_service import AttendanceService
from app.repositories.attendance_repository import AttendanceRepository
from app.core.dependencies import get_current_user, get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.attendance_schema import AttendanceResponse, RegisterFaceResponse

router = APIRouter(prefix="/attendance", tags=["Attendance"])

def get_attendance_service(db: AsyncSession = Depends(get_db_session)):
    repo = AttendanceRepository(db)
    return AttendanceService(repo)

def require_mahasiswa(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "mahasiswa":
        raise HTTPException(status_code=403, detail="Hanya mahasiswa yang dapat mengakses endpoint ini")
    return current_user

@router.post("/register-face", response_model=dict, responses={
    200: {"description": "Wajah berhasil didaftarkan"},
    400: {"description": "Gambar tidak valid atau wajah tidak ditemukan"}
})
async def register_face(
    file: UploadFile = File(...),
    current_user=Depends(require_mahasiswa),
    attendance_service: AttendanceService = Depends(get_attendance_service)
):
    """
    Mendaftarkan wajah mahasiswa untuk absensi.
    Kirim file gambar wajah (ideal close-up) melalui form-data.
    """
    image_bytes = await file.read()
    result = await attendance_service.register_face(current_user["sub"], image_bytes)
    return {"status": "success", "data": result}

@router.post("/check-in", response_model=dict, responses={
    200: {"description": "Absensi datang berhasil"},
    400: {"description": "Wajah tidak cocok, belum registrasi, atau sudah absen"}
})
async def check_in(
    file: UploadFile = File(...),
    current_user=Depends(require_mahasiswa),
    attendance_service: AttendanceService = Depends(get_attendance_service)
):
    """
    Melakukan absensi Datang dengan mengirimkan foto wajah (real-time).
    """
    image_bytes = await file.read()
    att = await attendance_service.check_in(current_user["sub"], image_bytes)
    return {"status": "success", "data": {"id": str(att.id), "date": att.date, "type": att.type}}

@router.post("/check-out", response_model=dict, responses={
    200: {"description": "Absensi pulang berhasil"},
    400: {"description": "Wajah tidak cocok, belum registrasi, atau sudah absen"}
})
async def check_out(
    file: UploadFile = File(...),
    current_user=Depends(require_mahasiswa),
    attendance_service: AttendanceService = Depends(get_attendance_service)
):
    """
    Melakukan absensi Pulang dengan mengirimkan foto wajah (real-time).
    """
    image_bytes = await file.read()
    att = await attendance_service.check_out(current_user["sub"], image_bytes)
    return {"status": "success", "data": {"id": str(att.id), "date": att.date, "type": att.type}}

@router.get("", response_model=dict, responses={
    200: {"description": "Berhasil mendapatkan data absensi"}
})
async def get_attendances(
    date: Optional[str] = Query(None, description="Format YYYY-MM-DD. Jika kosong menggunakan hari ini."),
    current_user=Depends(get_current_user),
    attendance_service: AttendanceService = Depends(get_attendance_service)
):
    """
    Mendapatkan data absensi (Datang & Pulang) mahasiswa pada tanggal tertentu.
    Jika tidak ada tanggal yang dikirim, maka akan otomatis menggunakan tanggal hari ini.
    """
    mahasiswa_id = current_user["sub"]
    # Jika role mentor ingin melihat absensi, di masa depan perlu di sesuaikan, saat ini khusus owner (mahasiswa)
    attendances = await attendance_service.get_attendances(mahasiswa_id, date)
    
    formatted_data = []
    for a in attendances:
        formatted_data.append({
            "id": str(a.id),
            "type": a.type,
            "timestamp": a.timestamp,
            "date": a.date,
            "face_verified": a.face_verified
        })
        
    return {"status": "success", "data": formatted_data}

@router.get("/check-registration", response_model=dict, responses={
    200: {"description": "Berhasil mengecek status registrasi wajah"}
})
async def check_registration(
    current_user=Depends(require_mahasiswa),
    attendance_service: AttendanceService = Depends(get_attendance_service)
):
    """
    Mengecek apakah mahasiswa sudah mendaftarkan wajahnya atau belum.
    """
    is_registered = await attendance_service.is_face_registered(current_user["sub"])
    return {"status": "success", "data": {"is_registered": is_registered}}
