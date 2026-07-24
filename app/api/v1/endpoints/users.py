from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserProfileResponse
from app.services.user_service import UserService
from app.core.dependencies import get_current_user, get_user_repository
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])

def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return UserService(user_repo)

@router.get("/me", response_model=dict)
async def get_me(
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    profile = await user_service.get_my_profile(current_user["sub"])
    return {"status": "success", "data": profile.dict()}

from fastapi import Body, File, UploadFile
from app.schemas.user_schema import UserProfileUpdate
from app.utils.file_upload import save_upload_file

@router.patch("/me", response_model=dict, responses={200: {"description": "Profile updated successfully"}, 404: {"description": "User not found"}})
async def update_me(
    req: UserProfileUpdate = Body(...),
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Memperbarui data profil (Nama, Divisi, Universitas, Jabatan).
    Data yang tidak ingin diubah dikosongkan (null/omitted).
    """
    updated_profile = await user_service.update_my_profile(
        user_id=current_user["sub"],
        name=req.name,
        universitas=req.universitas,
        divisi=req.divisi,
        jabatan=req.jabatan
    )
    return {"status": "success", "data": updated_profile.dict()}

@router.post("/me/avatar", response_model=dict, responses={200: {"description": "Avatar updated successfully"}, 400: {"description": "No file provided"}})
async def update_my_avatar(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Mengunggah dan memperbarui foto profil (avatar) pengguna.
    """
    file_url = save_upload_file(file, subfolder="avatars")
    updated_profile = await user_service.update_my_avatar(current_user["sub"], file_url)
    return {"status": "success", "data": updated_profile.dict()}
