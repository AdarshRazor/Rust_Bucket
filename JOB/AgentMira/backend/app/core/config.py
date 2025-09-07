"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "postgresql://username:password@localhost:5432/agentmira_dev"
    test_database_url: str = "postgresql://username:password@localhost:5432/agentmira_test"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # ML Model
    ml_model_path: str = "./models/complex_price_model_v2.pkl"
    
    # Application
    debug: bool = True
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
