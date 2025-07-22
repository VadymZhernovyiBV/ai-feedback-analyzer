"""Configuration settings for the application."""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenRouter API settings
    OPENROUTER_API_KEY: str = Field(..., description="OpenRouter API key")
    
    # Database settings
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./feedback.db",
        description="Database connection URL"
    )
    
    # CORS settings
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        description="Allowed CORS origins"
    )
    
    # Application settings
    APP_URL: Optional[str] = Field(
        default="http://localhost:8000",
        description="Application URL for OpenRouter headers"
    )
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    # API settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "AI Feedback Analyzer"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()