from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, attendance, task, report

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(attendance.router)
api_router.include_router(task.router)
api_router.include_router(report.router)
