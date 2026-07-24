from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "KIT KP Monitor API"
    app_env: str = "development"
    base_url: str
    api_v1_prefix: str = "/api/v1"

    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080

    upload_dir: str = "/app/uploads"
    max_upload_size_mb: int = 5

    face_match_threshold: float = 0.6
    face_model_name: str = "hog"

    cors_origins: str = "*"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
