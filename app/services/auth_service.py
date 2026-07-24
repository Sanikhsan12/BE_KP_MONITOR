from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User, MahasiswaProfile, MentorProfile
from app.schemas.auth_schema import RegisterMahasiswaRequest, RegisterMentorRequest, LoginRequest
from app.core.config import settings
from datetime import datetime
import uuid

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_mahasiswa(self, req: RegisterMahasiswaRequest):
        existing_user = await self.user_repo.get_user_by_email(req.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email sudah terdaftar")
        
        if await self.user_repo.check_nim_or_nik(req.nim, 'mahasiswa'):
            raise HTTPException(status_code=400, detail="NIM sudah terdaftar")

        user_id = uuid.uuid4()
        new_user = User(
            id=user_id,
            name=req.name,
            email=req.email,
            password_hash=hash_password(req.password),
            role="mahasiswa",
            created_at=datetime.utcnow().isoformat()
        )
        
        profile = MahasiswaProfile(
            user_id=user_id,
            nim=req.nim,
            universitas=req.universitas,
            divisi=req.divisi,
            periode_mulai=req.periode_mulai,
            periode_selesai=req.periode_selesai
        )
        
        await self.user_repo.create_user(new_user)
        await self.user_repo.create_mahasiswa_profile(profile)
        await self.user_repo.commit()
        
        return {"id": str(user_id), "email": new_user.email, "role": new_user.role}

    async def register_mentor(self, req: RegisterMentorRequest):
        existing_user = await self.user_repo.get_user_by_email(req.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email sudah terdaftar")
            
        if await self.user_repo.check_nim_or_nik(req.nik, 'mentor'):
            raise HTTPException(status_code=400, detail="NIK sudah terdaftar")

        user_id = uuid.uuid4()
        new_user = User(
            id=user_id,
            name=req.name,
            email=req.email,
            password_hash=hash_password(req.password),
            role="mentor",
            created_at=datetime.utcnow().isoformat()
        )
        
        profile = MentorProfile(
            user_id=user_id,
            nik=req.nik,
            divisi=req.divisi,
            jabatan=req.jabatan
        )
        
        await self.user_repo.create_user(new_user)
        await self.user_repo.create_mentor_profile(profile)
        await self.user_repo.commit()
        
        return {"id": str(user_id), "email": new_user.email, "role": new_user.role}

    async def login(self, req: LoginRequest):
        user = await self.user_repo.get_user_by_email(req.email)
        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Email atau password salah")

        access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60,
            "user": {
                "id": str(user.id),
                "name": user.name,
                "role": user.role
            }
        }
