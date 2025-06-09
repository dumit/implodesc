"""
Application configuration using Pydantic Settings
"""
from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment name")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    reload: bool = Field(default=False, description="Auto-reload on changes")
    
    # Security
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for JWT and encryption"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    allowed_hosts: Optional[List[str]] = Field(
        default=None,
        description="Allowed hosts for security"
    )
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        description="CORS allowed origins"
    )
    
    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://implodesc:password@localhost/implodesc",
        description="Database connection URL"
    )
    database_echo: bool = Field(
        default=False,
        description="Echo SQL queries"
    )
    
    # Redis/Cache
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    cache_ttl: int = Field(
        default=3600,
        description="Default cache TTL in seconds"
    )
    
    # AI Services
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key"
    )
    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic API key"
    )
    default_ai_model: str = Field(
        default="gpt-4o",
        description="Default AI model to use"
    )
    ai_max_tokens: int = Field(
        default=4096,
        description="Maximum tokens for AI responses"
    )
    ai_temperature: float = Field(
        default=0.1,
        description="AI temperature setting"
    )
    
    # Analysis settings
    max_analysis_time: int = Field(
        default=300,
        description="Maximum analysis time in seconds"
    )
    max_clarification_rounds: int = Field(
        default=3,
        description="Maximum clarification rounds"
    )
    
    # File storage
    upload_max_size: int = Field(
        default=10 * 1024 * 1024,  # 10MB
        description="Maximum upload file size in bytes"
    )
    storage_path: str = Field(
        default="./storage",
        description="Local storage path"
    )
    
    # Task queue
    celery_broker_url: str = Field(
        default="redis://localhost:6379/1",
        description="Celery broker URL"
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/2",
        description="Celery result backend URL"
    )
    
    # External APIs
    external_api_timeout: int = Field(
        default=30,
        description="External API timeout in seconds"
    )
    external_api_retries: int = Field(
        default=3,
        description="External API retry attempts"
    )
    
    # Monitoring
    enable_metrics: bool = Field(
        default=True,
        description="Enable Prometheus metrics"
    )
    metrics_path: str = Field(
        default="/metrics",
        description="Metrics endpoint path"
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()