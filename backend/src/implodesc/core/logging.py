"""
Logging configuration using structlog
"""
import logging
import sys
from typing import Any, Dict

import structlog
from structlog.typing import Processor

from .config import get_settings


def setup_logging() -> None:
    """Configure structured logging with structlog"""
    settings = get_settings()
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )
    
    # Configure structlog
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.StackInfoRenderer(),
    ]
    
    if settings.debug:
        # Pretty printing for development
        processors.extend([
            structlog.dev.ConsoleRenderer(colors=True),
        ])
    else:
        # JSON for production
        processors.extend([
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ])
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level.upper())
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)


def log_request_response(
    method: str,
    url: str,
    status_code: int,
    response_time: float,
    **kwargs: Any
) -> None:
    """Log HTTP request/response"""
    logger = get_logger("http")
    
    log_data: Dict[str, Any] = {
        "method": method,
        "url": url, 
        "status_code": status_code,
        "response_time_ms": round(response_time * 1000, 2),
        **kwargs
    }
    
    if status_code >= 500:
        logger.error("HTTP request failed", **log_data)
    elif status_code >= 400:
        logger.warning("HTTP client error", **log_data)
    else:
        logger.info("HTTP request completed", **log_data)