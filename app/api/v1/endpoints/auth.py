from fastapi import APIRouter, Depends, Body, HTTPException
from typing import Union, Dict, Any
from app.schemas.auth_schema import RegisterMahasiswaRequest, RegisterMentorRequest, LoginRequest, LoginResponse
from app.services.auth_service import AuthService
from app.core.dependencies import get_auth_service, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=201)
async def register(
    req: dict = Body(...),
    auth_service: AuthService = Depends(get_auth_service)
):
    role = req.get("role")
    if role == "mahasiswa":
        valid_req = RegisterMahasiswaRequest(**req)
        result = await auth_service.register_mahasiswa(valid_req)
    elif role == "mentor":
        valid_req = RegisterMentorRequest(**req)
        result = await auth_service.register_mentor(valid_req)
    else:
        raise HTTPException(status_code=400, detail="Role tidak valid")
        
    return {"status": "success", "data": result}

@router.post("/login", response_model=LoginResponse)
async def login(
    req: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    result = await auth_service.login(req)
    return {"status": "success", "data": result}

@router.post("/logout")
async def logout(current_user=Depends(get_current_user)):
    return {"status": "success", "data": None}
