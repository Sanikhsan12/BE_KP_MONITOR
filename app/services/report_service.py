from fastapi import HTTPException
from app.repositories.report_repository import ReportRepository
from app.schemas.report_schema import DailyReportCreateRequest, DailyReportResponse, WeeklyReportResponse
from app.models.report import DailyReport, WeeklyReport
from app.utils.file_upload import save_upload_file
from datetime import datetime, timedelta
import uuid

class ReportService:
    def __init__(self, report_repo: ReportRepository):
        self.report_repo = report_repo

    async def create_daily_report(self, mahasiswa_id: str, req: DailyReportCreateRequest) -> dict:
        report_date = req.report_date if req.report_date else datetime.now().strftime("%Y-%m-%d")
        new_report = DailyReport(
            id=uuid.uuid4(),
            task_id=uuid.UUID(req.task_id) if req.task_id else None,
            mahasiswa_id=mahasiswa_id,
            activity=req.activity,
            obstacle=req.obstacle,
            tomorrow_plan=req.tomorrow_plan,
            report_date=report_date,
            send_status="sent",
            submitted_at=datetime.now().isoformat()
        )
        await self.report_repo.create_daily_report(new_report)
        await self.report_repo.commit()
        return {"id": str(new_report.id), "message": "Laporan harian berhasil dibuat"}

    async def get_daily_reports(self, mahasiswa_id: str, date_filter: str = None) -> list:
        # Default rentang dinamis H-3 sampai H+3
        today = datetime.now()
        start_date = (today - timedelta(days=3)).strftime("%Y-%m-%d")
        end_date = (today + timedelta(days=3)).strftime("%Y-%m-%d")
        
        # Bisa diextend jika date_filter digunakan secara spesifik
        if date_filter:
            try:
                d = datetime.strptime(date_filter, "%Y-%m-%d")
                start_date = (d - timedelta(days=3)).strftime("%Y-%m-%d")
                end_date = (d + timedelta(days=3)).strftime("%Y-%m-%d")
            except ValueError:
                pass # Tetap pakai H-3 H+3 dari hari ini

        reports = await self.report_repo.get_daily_reports(mahasiswa_id, start_date, end_date)
        
        result = []
        for r in reports:
            result.append(DailyReportResponse(
                id=str(r.id),
                task_id=str(r.task_id) if r.task_id else None,
                mahasiswa_id=str(r.mahasiswa_id),
                activity=r.activity,
                obstacle=r.obstacle,
                tomorrow_plan=r.tomorrow_plan,
                report_date=r.report_date,
                send_status=r.send_status,
                submitted_at=r.submitted_at
            ))
        return result

    async def create_weekly_report(self, mahasiswa_id: str, date_str: str, file) -> dict:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Hanya file PDF yang diperbolehkan")
            
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Format tanggal tidak valid (YYYY-MM-DD)")
            
        year, week_number, _ = target_date.isocalendar()
        
        if await self.report_repo.check_weekly_report_exists(mahasiswa_id, week_number, year):
            raise HTTPException(status_code=400, detail=f"Laporan mingguan untuk minggu ke-{week_number} tahun {year} sudah ada")
            
        file_url = save_upload_file(file, subfolder="weekly_reports")
        
        new_report = WeeklyReport(
            id=uuid.uuid4(),
            mahasiswa_id=mahasiswa_id,
            week_number=week_number,
            year=year,
            file_url=file_url,
            status="submitted",
            submitted_at=datetime.now().isoformat()
        )
        
        await self.report_repo.create_weekly_report(new_report)
        await self.report_repo.commit()
        return {"id": str(new_report.id), "message": "Laporan mingguan berhasil diunggah"}

    async def get_weekly_reports(self, mahasiswa_id: str, date_filter: str = None) -> list:
        reports = await self.report_repo.get_weekly_reports(mahasiswa_id)
        
        # Filter spesifik di memory
        if date_filter:
            try:
                target_date = datetime.strptime(date_filter, "%Y-%m-%d")
                year, week_number, _ = target_date.isocalendar()
                reports = [r for r in reports if r.year == year and r.week_number == week_number]
            except ValueError:
                pass
                
        result = []
        for r in reports:
            result.append(WeeklyReportResponse(
                id=str(r.id),
                mahasiswa_id=str(r.mahasiswa_id),
                week_number=r.week_number,
                year=r.year,
                file_url=r.file_url,
                notes=r.notes,
                status=r.status,
                submitted_at=r.submitted_at,
                reviewed_at=r.reviewed_at,
                reviewed_by=str(r.reviewed_by) if r.reviewed_by else None
            ))
        return result
