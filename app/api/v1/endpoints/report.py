from fastapi import APIRouter, Depends, File, UploadFile, Query, HTTPException, Body, Form
from typing import List, Optional
from app.services.report_service import ReportService
from app.repositories.report_repository import ReportRepository
from app.core.dependencies import get_current_user, get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.report_schema import DailyReportCreateRequest

router = APIRouter(prefix="/reports", tags=["Reports"])

def get_report_service(db: AsyncSession = Depends(get_db_session)):
    repo = ReportRepository(db)
    return ReportService(repo)

def require_mahasiswa(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "mahasiswa":
        raise HTTPException(status_code=403, detail="Hanya mahasiswa yang dapat mengakses endpoint ini")
    return current_user

@router.get("/daily", response_model=dict, responses={200: {"description": "Daftar laporan harian"}})
async def get_daily_reports(
    date: Optional[str] = Query(None, description="Tanggal filter (opsional). Akan melimit data otomatis 50 terbaru dan mencari H-3 s.d H+3"),
    current_user=Depends(require_mahasiswa),
    report_service: ReportService = Depends(get_report_service)
):
    """Mendapatkan laporan harian."""
    result = await report_service.get_daily_reports(current_user["sub"], date)
    return {"status": "success", "data": [r.dict() for r in result]}

@router.post("/daily", response_model=dict, responses={201: {"description": "Laporan berhasil dibuat"}})
async def create_daily_report(
    req: DailyReportCreateRequest = Body(...),
    current_user=Depends(require_mahasiswa),
    report_service: ReportService = Depends(get_report_service)
):
    """Membuat laporan harian."""
    result = await report_service.create_daily_report(current_user["sub"], req)
    return {"status": "success", "data": result}

@router.get("/weekly", response_model=dict, responses={200: {"description": "Daftar laporan mingguan"}})
async def get_weekly_reports(
    date: Optional[str] = Query(None, description="Tanggal filter (berdasarkan date picker kalender)."),
    current_user=Depends(require_mahasiswa),
    report_service: ReportService = Depends(get_report_service)
):
    """Mendapatkan laporan mingguan."""
    result = await report_service.get_weekly_reports(current_user["sub"], date)
    return {"status": "success", "data": [r.dict() for r in result]}

@router.post("/weekly", response_model=dict, responses={201: {"description": "Laporan mingguan berhasil diupload"}, 400: {"description": "Format tidak valid atau laporan sudah ada"}})
async def upload_weekly_report(
    date: str = Form(..., description="Tanggal yang dipilih dari UI Kalender"),
    file: UploadFile = File(..., description="File PDF laporan mingguan"),
    current_user=Depends(require_mahasiswa),
    report_service: ReportService = Depends(get_report_service)
):
    """Mengunggah laporan mingguan (Hanya PDF)."""
    result = await report_service.create_weekly_report(current_user["sub"], date, file)
    return {"status": "success", "data": result}
