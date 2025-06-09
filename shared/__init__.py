"""
Shared schemas and models for Implodesc
"""
from .api_schemas import (
    AnalysisResultResponse,
    AnalysisStatusResponse,
    ErrorResponse,
    ExportRequest,
    ExportResponse,
    GetAnalysisRequest,
    HealthResponse,
    StartAnalysisRequest,
    StartAnalysisResponse,
    SubmitClarificationsRequest,
    SubmitClarificationsResponse,
)
from .carbon_models import (
    CarbonCalculator,
    EmissionFactor,
    EmissionScope,
    MaterialEmissionFactors,
    ProcessEmissionFactors,
    TransportEmissionFactors,
)
from .schemas import (
    AnalysisRequest,
    CarbonFootprint,
    ClarificationQuestion,
    ClarificationResponse,
    Company,
    ItemQuery,
    Location,
    Material,
    MaterialType,
    Process,
    ProcessType,
    SupplyChain,
    TransportMode,
    Transportation,
)

__all__ = [
    # Core schemas
    "AnalysisRequest",
    "CarbonFootprint", 
    "ClarificationQuestion",
    "ClarificationResponse",
    "Company",
    "ItemQuery",
    "Location",
    "Material",
    "MaterialType",
    "Process",
    "ProcessType",
    "SupplyChain",
    "TransportMode",
    "Transportation",
    
    # API schemas
    "AnalysisResultResponse",
    "AnalysisStatusResponse", 
    "ErrorResponse",
    "ExportRequest",
    "ExportResponse",
    "GetAnalysisRequest",
    "HealthResponse",
    "StartAnalysisRequest",
    "StartAnalysisResponse",
    "SubmitClarificationsRequest",
    "SubmitClarificationsResponse",
    
    # Carbon models
    "CarbonCalculator",
    "EmissionFactor",
    "EmissionScope",
    "MaterialEmissionFactors",
    "ProcessEmissionFactors", 
    "TransportEmissionFactors",
]