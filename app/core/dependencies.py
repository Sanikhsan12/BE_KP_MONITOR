from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        payload = decode_access_token(credentials.credentials)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau kadaluwarsa",
        )

def require_role(role: str):
    async def checker(user=Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Akses ditolak untuk role ini")
        return user
    return checker

def get_user_repository(session: AsyncSession = Depends(get_db_session)):
    return UserRepository(session)

def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)):
    return AuthService(user_repo)
