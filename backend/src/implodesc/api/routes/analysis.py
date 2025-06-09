"""
Supply chain analysis endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
import structlog

from ...core.config import Settings, get_settings
from ...services.analysis_service import AnalysisService
# Temporary inline schemas until shared module is properly integrated
from typing import List, Optional
from pydantic import BaseModel

# Inline schemas for now
class ItemQuery(BaseModel):
    item_name: str
    description: Optional[str] = None
    quantity: Optional[int] = 1
    category: Optional[str] = None

class ClarificationQuestion(BaseModel):
    id: str
    question: str
    type: str
    options: Optional[List[str]] = None
    required: bool = True

class ClarificationResponse(BaseModel):
    question_id: str
    answer: str

class StartAnalysisRequest(BaseModel):
    query: ItemQuery

class StartAnalysisResponse(BaseModel):
    session_id: str
    clarifications: List[ClarificationQuestion]
    message: str = "Please provide clarifications to proceed with analysis"

class SubmitClarificationsRequest(BaseModel):
    session_id: str
    clarifications: List[ClarificationResponse]

class SubmitClarificationsResponse(BaseModel):
    session_id: str
    status: str
    estimated_completion_time: Optional[int] = None
    message: str

class AnalysisStatusResponse(BaseModel):
    session_id: str
    status: str
    progress_percentage: Optional[int] = None
    current_step: Optional[str] = None
    estimated_time_remaining: Optional[int] = None
    message: str

class AnalysisResultResponse(BaseModel):
    session_id: str
    item_name: str
    analysis_result: dict  # Full analysis data
    created_at: str
    clarifications_used: dict

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[str] = None

class SetAPIKeysRequest(BaseModel):
    session_id: str
    api_keys: dict  # {"openai": "key", "anthropic": "key"}

class SetAPIKeysResponse(BaseModel):
    session_id: str
    services_available: dict
    message: str

logger = structlog.get_logger(__name__)
router = APIRouter()

# Global analysis service instance (in production, use dependency injection)
_analysis_service = None

def get_analysis_service(settings: Settings = Depends(get_settings)) -> AnalysisService:
    """Get analysis service instance"""
    global _analysis_service
    if _analysis_service is None:
        _analysis_service = AnalysisService(settings)
    return _analysis_service


@router.post("/analysis/start", response_model=StartAnalysisResponse)
async def start_analysis(
    request: StartAnalysisRequest,
    analysis_service: AnalysisService = Depends(get_analysis_service)
) -> StartAnalysisResponse:
    """Start a new supply chain analysis"""
    logger.info("Starting analysis", item_name=request.query.item_name)
    
    try:
        result = await analysis_service.start_analysis(
            item_name=request.query.item_name,
            item_description=request.query.description,
            quantity=request.query.quantity or 1
        )
        
        # Convert result to response format
        clarifications = [
            ClarificationQuestion(**q) for q in result["clarifications"]
        ]
        
        return StartAnalysisResponse(
            session_id=result["session_id"],
            clarifications=clarifications,
            message=result["message"]
        )
        
    except Exception as e:
        logger.error("Failed to start analysis", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start analysis: {str(e)}"
        )


@router.post("/analysis/clarify", response_model=SubmitClarificationsResponse)
async def submit_clarifications(
    request: SubmitClarificationsRequest,
    analysis_service: AnalysisService = Depends(get_analysis_service)
) -> SubmitClarificationsResponse:
    """Submit clarification responses"""
    logger.info(
        "Clarifications submitted", 
        session_id=request.session_id,
        num_clarifications=len(request.clarifications)
    )
    
    try:
        # Convert clarifications to dict format
        clarifications = [
            {"question_id": c.question_id, "answer": c.answer}
            for c in request.clarifications
        ]
        
        result = await analysis_service.submit_clarifications(
            session_id=request.session_id,
            clarifications=clarifications
        )
        
        return SubmitClarificationsResponse(
            session_id=result["session_id"],
            status=result["status"],
            estimated_completion_time=result.get("estimated_completion_time"),
            message=result["message"]
        )
        
    except ValueError as e:
        logger.error("Invalid session or data", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to submit clarifications", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit clarifications: {str(e)}"
        )


@router.get("/analysis/{session_id}/status", response_model=AnalysisStatusResponse)
async def get_analysis_status(
    session_id: str,
    analysis_service: AnalysisService = Depends(get_analysis_service)
) -> AnalysisStatusResponse:
    """Get analysis status"""
    logger.info("Status check", session_id=session_id)
    
    try:
        result = await analysis_service.get_analysis_status(session_id)
        
        return AnalysisStatusResponse(
            session_id=result["session_id"],
            status=result["status"],
            progress_percentage=result.get("progress_percentage"),
            current_step=result.get("current_step"),
            estimated_time_remaining=result.get("estimated_time_remaining"),
            message=result["message"]
        )
        
    except ValueError as e:
        logger.error("Session not found", session_id=session_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to get status", session_id=session_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analysis status: {str(e)}"
        )


@router.get("/analysis/{session_id}/result", response_model=AnalysisResultResponse)
async def get_analysis_result(
    session_id: str,
    analysis_service: AnalysisService = Depends(get_analysis_service)
) -> AnalysisResultResponse:
    """Get completed analysis results"""
    logger.info("Result requested", session_id=session_id)
    
    try:
        result = await analysis_service.get_analysis_result(session_id)
        
        return AnalysisResultResponse(
            session_id=result["session_id"],
            item_name=result["item_name"],
            analysis_result=result["analysis_result"],
            created_at=result["created_at"],
            clarifications_used=result["clarifications_used"]
        )
        
    except ValueError as e:
        logger.error("Session not found or not completed", session_id=session_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to get analysis result", session_id=session_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analysis result: {str(e)}"
        )


@router.post("/analysis/api-keys", response_model=SetAPIKeysResponse)
async def set_api_keys(
    request: SetAPIKeysRequest,
    analysis_service: AnalysisService = Depends(get_analysis_service)
) -> SetAPIKeysResponse:
    """Set user-provided API keys for a session"""
    logger.info("API keys provided", session_id=request.session_id, 
               keys=list(request.api_keys.keys()))
    
    try:
        # Set the API keys for the session
        analysis_service.set_api_keys(request.session_id, request.api_keys)
        
        # Get available services after setting keys
        services_available = analysis_service.get_available_services(request.session_id)
        
        return SetAPIKeysResponse(
            session_id=request.session_id,
            services_available=services_available,
            message="API keys set successfully"
        )
        
    except Exception as e:
        logger.error("Failed to set API keys", session_id=request.session_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set API keys: {str(e)}"
        )