"""
Shared data schemas for Implodesc supply chain analysis
"""
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


class MaterialType(str, Enum):
    """Types of materials in supply chain"""
    RAW_MATERIAL = "raw_material"
    PROCESSED_MATERIAL = "processed_material" 
    COMPONENT = "component"
    ASSEMBLY = "assembly"
    FINISHED_PRODUCT = "finished_product"
    PACKAGING = "packaging"
    ENERGY = "energy"
    WATER = "water"
    CHEMICAL = "chemical"


class ProcessType(str, Enum):
    """Types of supply chain processes"""
    EXTRACTION = "extraction"
    PROCESSING = "processing"
    MANUFACTURING = "manufacturing"
    ASSEMBLY = "assembly"
    PACKAGING = "packaging"
    TRANSPORTATION = "transportation"
    STORAGE = "storage"
    DISTRIBUTION = "distribution"
    RETAIL = "retail"
    USE = "use"
    END_OF_LIFE = "end_of_life"


class TransportMode(str, Enum):
    """Transportation modes"""
    TRUCK = "truck"
    RAIL = "rail"
    SHIP = "ship"
    AIR = "air"
    PIPELINE = "pipeline"


class Material(BaseModel):
    """Core material definition"""
    id: str
    name: str
    type: MaterialType
    description: Optional[str] = None
    unit: str  # kg, liters, pieces, etc.
    density: Optional[Decimal] = None  # kg/m³
    carbon_intensity: Optional[Decimal] = None  # kg CO2e per unit
    
    class Config:
        use_enum_values = True


class Location(BaseModel):
    """Geographic location"""
    name: str
    country: str
    region: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None  # {"lat": x, "lng": y}


class Company(BaseModel):
    """Company or entity in supply chain"""
    id: str
    name: str
    type: str  # supplier, manufacturer, distributor, etc.
    location: Location
    industry: Optional[str] = None
    size: Optional[str] = None  # small, medium, large
    sustainability_rating: Optional[str] = None


class CarbonFootprint(BaseModel):
    """Carbon footprint calculation"""
    total_co2e: Decimal  # kg CO2 equivalent
    scope1: Optional[Decimal] = None  # Direct emissions
    scope2: Optional[Decimal] = None  # Indirect energy emissions
    scope3: Optional[Decimal] = None  # Other indirect emissions
    methodology: str
    confidence_level: float = Field(ge=0.0, le=1.0)
    breakdown: Optional[Dict[str, Decimal]] = None  # Category breakdown


class Transportation(BaseModel):
    """Transportation step"""
    mode: TransportMode
    distance_km: Decimal
    origin: Location
    destination: Location
    carbon_intensity: Optional[Decimal] = None  # kg CO2e per km per unit
    
    class Config:
        use_enum_values = True


class Process(BaseModel):
    """Supply chain process step"""
    id: str
    name: str
    type: ProcessType
    description: Optional[str] = None
    location: Location
    company: Optional[Company] = None
    
    # Inputs and outputs
    inputs: List[Dict[str, Union[str, Decimal]]]  # {"material_id": "x", "quantity": y}
    outputs: List[Dict[str, Union[str, Decimal]]]
    
    # Environmental impact
    energy_consumption: Optional[Decimal] = None  # kWh
    water_consumption: Optional[Decimal] = None  # liters
    waste_generated: Optional[Decimal] = None  # kg
    carbon_footprint: Optional[CarbonFootprint] = None
    
    # Transportation to next step
    transportation: Optional[Transportation] = None
    
    # Process details
    duration_days: Optional[int] = None
    cost_estimate: Optional[Decimal] = None
    
    class Config:
        use_enum_values = True


class SupplyChain(BaseModel):
    """Complete supply chain analysis"""
    id: str
    product_name: str
    product_description: str
    quantity: Decimal
    unit: str
    
    # Analysis metadata
    created_at: datetime
    analysis_version: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    
    # Supply chain structure
    materials: List[Material]
    processes: List[Process]
    companies: List[Company]
    
    # Summary metrics
    total_carbon_footprint: CarbonFootprint
    total_distance_km: Decimal
    total_processing_time_days: int
    estimated_cost: Optional[Decimal] = None
    
    # Visualization data
    process_flow: List[Dict[str, str]]  # For flow diagrams
    geographic_path: List[Location]  # For maps
    
    class Config:
        use_enum_values = True


class ItemQuery(BaseModel):
    """User's item query for analysis"""
    item_name: str
    description: Optional[str] = None
    quantity: Optional[Decimal] = None
    unit: Optional[str] = None
    specifications: Optional[Dict[str, str]] = None
    use_case: Optional[str] = None
    target_market: Optional[str] = None


class ClarificationQuestion(BaseModel):
    """AI-generated clarification question"""
    id: str
    question: str
    type: str  # quantity, specification, use_case, etc.
    options: Optional[List[str]] = None  # For multiple choice
    required: bool = True


class ClarificationResponse(BaseModel):
    """User's response to clarification"""
    question_id: str
    answer: str
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class AnalysisRequest(BaseModel):
    """Request for supply chain analysis"""
    query: ItemQuery
    clarifications: List[ClarificationResponse] = []
    analysis_depth: str = "standard"  # basic, standard, detailed
    include_alternatives: bool = False