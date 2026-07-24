import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException
from app.core.config import settings

def save_upload_file(upload_file: UploadFile, subfolder: str = "") -> str:
    """
    Menyimpan file yang diupload dan mengembalikan relative path-nya.
    """
    if not upload_file or not upload_file.filename:
        return None
        
    # Validasi file size via seek (opsional, tapi disarankan)
    # Fastapi UploadFile file object
    
    file_ext = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    
    upload_dir = os.path.join(settings.upload_dir, subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan file: {str(e)}")
    finally:
        upload_file.file.close()
        
    # Return path yang bisa diakses via web (misal: /uploads/avatar/xxx.jpg)
    return f"/uploads/{subfolder}/{unique_filename}".replace("//", "/")
