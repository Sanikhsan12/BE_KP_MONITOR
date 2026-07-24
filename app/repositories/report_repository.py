from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from app.models.report import DailyReport, WeeklyReport
from typing import Optional, List

class ReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_daily_report(self, report: DailyReport):
        self.session.add(report)

    async def get_daily_reports(self, mahasiswa_id: str, start_date: str = None, end_date: str = None) -> List[DailyReport]:
        query = select(DailyReport).where(DailyReport.mahasiswa_id == mahasiswa_id)
        if start_date and end_date:
            query = query.where(DailyReport.report_date >= start_date, DailyReport.report_date <= end_date)
            
        # Dibatasi 50 terakhir
        query = query.order_by(desc(DailyReport.report_date)).limit(50)
        
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_weekly_report(self, report: WeeklyReport):
        self.session.add(report)

    async def get_weekly_reports(self, mahasiswa_id: str, date: str = None) -> List[WeeklyReport]:
        query = select(WeeklyReport).where(WeeklyReport.mahasiswa_id == mahasiswa_id)
        # Jika difilter berdasarkan date (asumsikan kita memfilter berdasarkan week_number atau year dari date itu)
        # Secara sederhana filter berdasarkan submitted_at atau field custom lainnya
        # Di sini kita akan ambil semua atau jika mau difilter lebih spesifik
        query = query.order_by(desc(WeeklyReport.year), desc(WeeklyReport.week_number))
        
        result = await self.session.execute(query)
        return result.scalars().all()

    async def check_weekly_report_exists(self, mahasiswa_id: str, week_number: int, year: int) -> bool:
        result = await self.session.execute(
            select(WeeklyReport).where(
                WeeklyReport.mahasiswa_id == mahasiswa_id,
                WeeklyReport.week_number == week_number,
                WeeklyReport.year == year
            )
        )
        return result.scalars().first() is not None

    async def commit(self):
        await self.session.commit()
