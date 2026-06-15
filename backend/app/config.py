from pydantic_settings import BaseSettings
from pydantic import field_validator, model_validator
from typing import List
import os
import json


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/ai_resume_analyzer"
    )

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://yourdomain.com",
    ]

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App
    APP_NAME: str = "AI Resume Analyzer"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # File upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_RESUME_MIME_TYPES: List[str] = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]

    # Rate limiting
    AUTH_RATE_LIMIT: int = int(os.getenv("AUTH_RATE_LIMIT", "10"))
    ANALYSIS_RATE_LIMIT: int = int(os.getenv("ANALYSIS_RATE_LIMIT", "5"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

    # NLP
    SPACY_MODEL: str = "en_core_web_sm"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() in {"production", "prod"}

    @field_validator("CORS_ORIGINS", "ALLOWED_RESUME_MIME_TYPES", mode="before")
    @classmethod
    def parse_csv_or_json_list(cls, value):
        if isinstance(value, str):
            stripped = value.strip()
            if stripped.startswith("["):
                return json.loads(stripped)
            return [item.strip() for item in stripped.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.is_production:
            if not self.SECRET_KEY or self.SECRET_KEY == "your-secret-key-change-in-production":
                raise ValueError("SECRET_KEY must be set to a strong value in production")
            if self.DEBUG:
                raise ValueError("DEBUG must be false in production")
            if any("yourdomain.com" in origin for origin in self.CORS_ORIGINS):
                raise ValueError("CORS_ORIGINS must be configured for the production domain")
        return self

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
