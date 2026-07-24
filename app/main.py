from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title=settings.app_name,
    description="Backend API untuk aplikasi Monitoring KP — KIT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(api_router, prefix=settings.api_v1_prefix)

# Pastikan folder ada
os.makedirs(settings.upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

@app.get("/")
async def root():
    return {"message": "Welcome to KIT KP Monitor API"}
