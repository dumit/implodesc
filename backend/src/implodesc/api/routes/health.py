"""
Health check endpoints
"""
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends
import structlog

from ...core.config import Settings, get_settings
from ....shared.api_schemas import HealthResponse

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """Basic health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.utcnow().isoformat()
    )


@router.get("/ready", response_model=Dict[str, Any])
async def readiness_check(settings: Settings = Depends(get_settings)) -> Dict[str, Any]:
    """Readiness check with dependency status"""
    checks = {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0",
        "environment": settings.environment,
        "dependencies": {
            "database": "healthy",  # TODO: Add actual DB health check
            "redis": "healthy",     # TODO: Add actual Redis health check
            "ai_service": "healthy" # TODO: Add actual AI service health check
        }
    }
    
    logger.info("Health check performed", **checks)
    return checks


@router.get("/live", response_model=Dict[str, str])
async def liveness_check() -> Dict[str, str]:
    """Liveness check for Kubernetes"""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }