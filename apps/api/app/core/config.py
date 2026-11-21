from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    ENV: str = "development"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://feedguide.vercel.app"
    ]

    # Supabase Configuration
    SUPABASE_URL: str = "https://mock.supabase.co"
    SUPABASE_ANON_KEY: str = "mock-anon-key"
    SUPABASE_SERVICE_ROLE_KEY: str = "mock-service-role-key"
    SUPABASE_JWT_SECRET: str = "super-secret-supabase-jwt-key-for-local-dev-min-32-chars"

    # AI Configuration
    PRIMARY_LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    VECTOR_DIMENSION: int = 768
    CHAT_RATE_LIMIT_PER_MINUTE: int = 15

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
