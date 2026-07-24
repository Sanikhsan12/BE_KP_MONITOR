from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User, MahasiswaProfile, MentorProfile
import uuid
from typing import Optional
from sqlalchemy import or_

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()
    
    async def check_nim_or_nik(self, identifier: str, role: str) -> bool:
        if role == 'mahasiswa':
            result = await self.session.execute(select(MahasiswaProfile).where(MahasiswaProfile.nim == identifier))
            return result.scalars().first() is not None
        elif role == 'mentor':
            result = await self.session.execute(select(MentorProfile).where(MentorProfile.nik == identifier))
            return result.scalars().first() is not None
        return False

    async def create_user(self, user: User):
        self.session.add(user)
        await self.session.flush()

    async def create_mahasiswa_profile(self, profile: MahasiswaProfile):
        self.session.add(profile)

    async def create_mentor_profile(self, profile: MentorProfile):
        self.session.add(profile)

    async def get_full_user_profile(self, user_id: str):
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return None
        
        m_prof = None
        mentor_prof = None
        if user.role == "mahasiswa":
            res = await self.session.execute(select(MahasiswaProfile).where(MahasiswaProfile.user_id == user_id))
            m_prof = res.scalars().first()
        elif user.role == "mentor":
            res = await self.session.execute(select(MentorProfile).where(MentorProfile.user_id == user_id))
            mentor_prof = res.scalars().first()
            
        return user, m_prof, mentor_prof

    async def update_user_avatar(self, user_id: str, avatar_url: str):
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if user:
            user.avatar_url = avatar_url
            self.session.add(user)

    async def update_mahasiswa_profile(self, user_id: str, name: Optional[str], universitas: Optional[str], divisi: Optional[str]):
        # Update user name
        if name:
            user_res = await self.session.execute(select(User).where(User.id == user_id))
            user = user_res.scalars().first()
            if user:
                user.name = name
                self.session.add(user)
                
        # Update mahasiswa profile
        prof_res = await self.session.execute(select(MahasiswaProfile).where(MahasiswaProfile.user_id == user_id))
        prof = prof_res.scalars().first()
        if prof:
            if universitas:
                prof.universitas = universitas
            if divisi:
                prof.divisi = divisi
            self.session.add(prof)

    async def update_mentor_profile(self, user_id: str, name: Optional[str], jabatan: Optional[str], divisi: Optional[str]):
        # Update user name
        if name:
            user_res = await self.session.execute(select(User).where(User.id == user_id))
            user = user_res.scalars().first()
            if user:
                user.name = name
                self.session.add(user)
                
        # Update mentor profile
        prof_res = await self.session.execute(select(MentorProfile).where(MentorProfile.user_id == user_id))
        prof = prof_res.scalars().first()
        if prof:
            if jabatan:
                prof.jabatan = jabatan
            if divisi:
                prof.divisi = divisi
            self.session.add(prof)

    async def commit(self):
        await self.session.commit()
