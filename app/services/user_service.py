from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserProfileResponse, MahasiswaProfileSchema, MentorProfileSchema
from fastapi import HTTPException

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_my_profile(self, user_id: str) -> UserProfileResponse:
        data = await self.user_repo.get_full_user_profile(user_id)
        if not data:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
        
        user, m_prof, mentor_prof = data
        
        response = UserProfileResponse(
            id=str(user.id),
            name=user.name,
            email=user.email,
            role=user.role,
            avatar_url=user.avatar_url
        )
        
        if m_prof:
            response.mahasiswa_profile = MahasiswaProfileSchema(
                nim=m_prof.nim,
                universitas=m_prof.universitas,
                divisi=m_prof.divisi,
                mentor_id=str(m_prof.mentor_id) if m_prof.mentor_id else None,
                periode_mulai=m_prof.periode_mulai,
                periode_selesai=m_prof.periode_selesai
            )
            
        if mentor_prof:
            response.mentor_profile = MentorProfileSchema(
                nik=mentor_prof.nik,
                divisi=mentor_prof.divisi,
                jabatan=mentor_prof.jabatan
            )
            
        return response

    async def update_my_profile(self, user_id: str, name: str = None, universitas: str = None, divisi: str = None, jabatan: str = None) -> UserProfileResponse:
        data = await self.user_repo.get_full_user_profile(user_id)
        if not data:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
        user = data[0]
        
        if user.role == "mahasiswa":
            await self.user_repo.update_mahasiswa_profile(user_id, name, universitas, divisi)
        elif user.role == "mentor":
            await self.user_repo.update_mentor_profile(user_id, name, jabatan, divisi)
            
        await self.user_repo.commit()
        return await self.get_my_profile(user_id)
        
    async def update_my_avatar(self, user_id: str, avatar_url: str) -> UserProfileResponse:
        data = await self.user_repo.get_full_user_profile(user_id)
        if not data:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
            
        await self.user_repo.update_user_avatar(user_id, avatar_url)
        await self.user_repo.commit()
        
        return await self.get_my_profile(user_id)
