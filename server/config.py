import os
from datetime import timedelta
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    
    # FastAPI配置
    APP_NAME: str = "WisdomBase API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./wisdombase.db"
    DATABASE_ECHO: bool = True
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120  # 2小时
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    CORS_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
