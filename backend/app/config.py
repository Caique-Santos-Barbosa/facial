from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "HDT Energy - Sistema de Reconhecimento Facial"
    VERSION: str = "1.0.0"
    
    # Database
    POSTGRES_SERVER: str = "postgres"
    POSTGRES_USER: str = "facial_user"
    POSTGRES_PASSWORD: str = "facial_pass"
    POSTGRES_DB: str = "facial_db"
    DATABASE_URL: Optional[str] = None
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    
    # Security
    SECRET_KEY: str = "change-this-super-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias
    
    # Face Recognition
    FACE_RECOGNITION_TOLERANCE: float = 0.6
    FACE_DETECTION_MODEL: str = "hog"
    MIN_FACE_SIZE: int = 100
    
    # Liveness Detection
    LIVENESS_ENABLED: bool = True
    LIVENESS_THRESHOLD: float = 0.7
    
    # Door Control
    DOOR_CONTROLLER_BASE_URL: str = "http://187.50.63.194:8080"
    DOOR_CONTROLLER_USERNAME: str = "abc"
    DOOR_CONTROLLER_PASSWORD: str = "123"
    DOOR_OPEN_DURATION: int = 5  # segundos
    
    # Storage
    UPLOAD_DIR: str = "uploads"
    FACES_DIR: str = "uploads/faces"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:19006"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

