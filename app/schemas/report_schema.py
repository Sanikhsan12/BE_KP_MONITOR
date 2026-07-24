from pydantic import BaseModel
from typing import Optional

class DailyReportCreateRequest(BaseModel):
    activity: str
    obstacle: str
    tomorrow_plan: str
    report_date: Optional[str] = None
    task_id: Optional[str] = None

class DailyReportResponse(BaseModel):
    id: str
    task_id: Optional[str] = None
    mahasiswa_id: str
    activity: str
    obstacle: str
    tomorrow_plan: str
    report_date: str
    send_status: str
    submitted_at: Optional[str] = None

class WeeklyReportResponse(BaseModel):
    id: str
    mahasiswa_id: str
    week_number: int
    year: int
    file_url: str
    notes: Optional[str] = None
    status: str
    submitted_at: Optional[str] = None
    reviewed_at: Optional[str] = None
    reviewed_by: Optional[str] = None
