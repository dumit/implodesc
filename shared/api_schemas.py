"""
API request and response schemas for Implodesc
"""
from typing import List, Optional
from pydantic import BaseModel

from schemas import (
    AnalysisRequest,
    ClarificationQuestion,
    ClarificationResponse,
    ItemQuery,
    SupplyChain
)


# Request schemas
class StartAnalysisRequest(BaseModel):
    """Initial request to start supply chain analysis"""
    query: ItemQuery


class SubmitClarificationsRequest(BaseModel):
    """Submit clarification responses"""
    session_id: str
    clarifications: List[ClarificationResponse]


class GetAnalysisRequest(BaseModel):
    """Get analysis results"""
    session_id: str


# Response schemas
class StartAnalysisResponse(BaseModel):
    """Response to start analysis request"""
    session_id: str
    clarifications: List[ClarificationQuestion]
    message: str = "Please provide clarifications to proceed with analysis"


class SubmitClarificationsResponse(BaseModel):
    """Response after submitting clarifications"""
    session_id: str
    status: str  # "processing", "needs_more_clarification", "completed"
    additional_clarifications: Optional[List[ClarificationQuestion]] = None
    estimated_completion_time: Optional[int] = None  # seconds
    message: str


class AnalysisStatusResponse(BaseModel):
    """Analysis status check response"""
    session_id: str
    status: str  # "pending", "processing", "completed", "failed"
    progress_percentage: Optional[int] = None
    current_step: Optional[str] = None
    estimated_time_remaining: Optional[int] = None  # seconds
    message: str


class AnalysisResultResponse(BaseModel):
    """Complete analysis results"""
    session_id: str
    supply_chain: SupplyChain
    analysis_summary: str
    key_insights: List[str]
    recommendations: List[str]
    limitations: List[str]


class ErrorResponse(BaseModel):
    """Error response schema"""
    error_code: str
    message: str
    details: Optional[str] = None
    session_id: Optional[str] = None


# Health check
class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str
    timestamp: str


# Export schemas
class ExportRequest(BaseModel):
    """Request to export analysis results"""
    session_id: str
    format: str  # "pdf", "csv", "json"
    include_visualizations: bool = True


class ExportResponse(BaseModel):
    """Export response with download link"""
    session_id: str
    download_url: str
    expires_at: str
    file_size_bytes: int
    format: str