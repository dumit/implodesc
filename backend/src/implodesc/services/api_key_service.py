"""
API Key management service supporting multiple sources
"""
from typing import Optional, Dict, Any
import structlog
from ..core.config import Settings

logger = structlog.get_logger(__name__)


class APIKeyService:
    """Service for managing API keys from multiple sources"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        # In-memory storage for user-provided keys (session-based)
        self._user_keys: Dict[str, Dict[str, str]] = {}
    
    def set_user_api_keys(self, session_id: str, api_keys: Dict[str, str]):
        """
        Store user-provided API keys for a session
        
        Args:
            session_id: Session identifier
            api_keys: Dictionary of API keys {"openai": "key", "anthropic": "key"}
        """
        # Validate keys (basic format check)
        validated_keys = {}
        
        if "openai" in api_keys and api_keys["openai"]:
            key = api_keys["openai"].strip()
            if key.startswith("sk-") and len(key) > 20:
                validated_keys["openai"] = key
                logger.info("Valid OpenAI key provided", session_id=session_id)
            else:
                logger.warning("Invalid OpenAI key format", session_id=session_id)
        
        if "anthropic" in api_keys and api_keys["anthropic"]:
            key = api_keys["anthropic"].strip()
            if len(key) > 10:  # Basic length check
                validated_keys["anthropic"] = key
                logger.info("Valid Anthropic key provided", session_id=session_id)
            else:
                logger.warning("Invalid Anthropic key format", session_id=session_id)
        
        if validated_keys:
            self._user_keys[session_id] = validated_keys
            logger.info("User API keys stored", session_id=session_id, 
                       keys=list(validated_keys.keys()))
    
    def get_openai_api_key(self, session_id: Optional[str] = None) -> Optional[str]:
        """
        Get OpenAI API key from user-provided keys or environment
        
        Args:
            session_id: Optional session ID for user-provided keys
            
        Returns:
            API key or None if not available
        """
        # Try user-provided key first
        if session_id and session_id in self._user_keys:
            user_key = self._user_keys[session_id].get("openai")
            if user_key:
                logger.debug("Using user-provided OpenAI key", session_id=session_id)
                return user_key
        
        # Fallback to environment variable
        if self.settings.openai_api_key:
            logger.debug("Using environment OpenAI key")
            return self.settings.openai_api_key
        
        logger.debug("No OpenAI API key available")
        return None
    
    def get_anthropic_api_key(self, session_id: Optional[str] = None) -> Optional[str]:
        """
        Get Anthropic API key from user-provided keys or environment
        
        Args:
            session_id: Optional session ID for user-provided keys
            
        Returns:
            API key or None if not available
        """
        # Try user-provided key first
        if session_id and session_id in self._user_keys:
            user_key = self._user_keys[session_id].get("anthropic")
            if user_key:
                logger.debug("Using user-provided Anthropic key", session_id=session_id)
                return user_key
        
        # Fallback to environment variable
        if self.settings.anthropic_api_key:
            logger.debug("Using environment Anthropic key")
            return self.settings.anthropic_api_key
        
        logger.debug("No Anthropic API key available")
        return None
    
    def has_any_api_key(self, session_id: Optional[str] = None) -> bool:
        """Check if any AI API key is available"""
        return (self.get_openai_api_key(session_id) is not None or 
                self.get_anthropic_api_key(session_id) is not None)
    
    def get_available_services(self, session_id: Optional[str] = None) -> Dict[str, bool]:
        """Get which AI services are available"""
        return {
            "openai": self.get_openai_api_key(session_id) is not None,
            "anthropic": self.get_anthropic_api_key(session_id) is not None,
            "mock": True  # Mock service always available
        }
    
    def clear_user_keys(self, session_id: str):
        """Clear user-provided API keys for a session"""
        if session_id in self._user_keys:
            del self._user_keys[session_id]
            logger.info("User API keys cleared", session_id=session_id)
    
    def cleanup_expired_sessions(self, active_session_ids: set):
        """Remove API keys for expired sessions"""
        expired_sessions = set(self._user_keys.keys()) - active_session_ids
        for session_id in expired_sessions:
            self.clear_user_keys(session_id)
        
        if expired_sessions:
            logger.info("Cleaned up expired API key sessions", 
                       count=len(expired_sessions))