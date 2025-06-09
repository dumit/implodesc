"""
Unit tests for configuration management
"""
import pytest
from implodesc.core.config import Settings, get_settings


def test_settings_creation():
    """Test settings can be created with defaults"""
    settings = Settings()
    
    assert settings.environment == "development"
    assert settings.debug is False  # Default is False
    assert settings.log_level == "INFO"
    assert settings.host == "0.0.0.0"
    assert settings.port == 8000


def test_settings_from_env(monkeypatch):
    """Test settings can be loaded from environment"""
    monkeypatch.setenv("ENVIRONMENT", "testing")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("PORT", "9000")
    
    settings = Settings()
    
    assert settings.environment == "testing"
    assert settings.debug is True
    assert settings.log_level == "DEBUG"
    assert settings.port == 9000


def test_get_settings():
    """Test get_settings function"""
    settings = get_settings()
    
    assert isinstance(settings, Settings)
    assert settings.environment == "development"


def test_cors_origins_default():
    """Test CORS origins default configuration"""
    settings = Settings()
    
    assert "http://localhost:3000" in settings.cors_origins
    assert "http://localhost:3001" in settings.cors_origins