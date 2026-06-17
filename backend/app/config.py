from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from typing import List
import os

WEAK_SECRET_KEYS = {
    "your-secret-key-change-in-production",
    "your-secret-key-change-this-in-production",
    "your-super-secret-key-change-in-production",
    "secret",
    "changeme",
}

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/ai_resume_analyzer"
    )
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://yourdomain.com"
    ]
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App
    APP_NAME: str = "AI Resume Analyzer"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # File upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    # NLP
    SPACY_MODEL: str = "en_core_web_sm"

    @model_validator(mode="after")
    def validate_secret_key(self):
        key = self.SECRET_KEY
        if not key or key.lower() in WEAK_SECRET_KEYS or len(key) < 32:
            raise ValueError(
                "SECRET_KEY is missing or insecure. "
                "Generate a secure key with: "
                "python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        return self

   
        
settings = Settings()

print("Gemini configured")
