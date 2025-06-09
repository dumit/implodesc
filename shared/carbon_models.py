"""
Carbon footprint calculation models and utilities for Implodesc
"""
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from .schemas import CarbonFootprint, Material, Process, TransportMode


class EmissionScope(str, Enum):
    """GHG Protocol emission scopes"""
    SCOPE_1 = "scope1"  # Direct emissions
    SCOPE_2 = "scope2"  # Indirect energy emissions  
    SCOPE_3 = "scope3"  # Other indirect emissions


class CarbonCalculationMethod(str, Enum):
    """Carbon calculation methodologies"""
    LCA = "life_cycle_assessment"
    EMISSION_FACTOR = "emission_factor"
    SPEND_BASED = "spend_based"
    SUPPLIER_SPECIFIC = "supplier_specific"
    HYBRID = "hybrid"


class EmissionFactor(BaseModel):
    """Emission factor for carbon calculations"""
    name: str
    factor: Decimal  # kg CO2e per unit
    unit: str
    source: str
    region: Optional[str] = None
    year: int
    uncertainty: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class MaterialEmissionFactors(BaseModel):
    """Emission factors for materials"""
    STEEL = EmissionFactor(
        name="Steel",
        factor=Decimal("1.85"),
        unit="kg CO2e/kg",
        source="DEFRA 2023",
        year=2023
    )
    ALUMINUM = EmissionFactor(
        name="Aluminum",
        factor=Decimal("8.24"),
        unit="kg CO2e/kg", 
        source="DEFRA 2023",
        year=2023
    )
    PLASTIC_PET = EmissionFactor(
        name="PET Plastic",
        factor=Decimal("2.15"),
        unit="kg CO2e/kg",
        source="DEFRA 2023", 
        year=2023
    )
    COTTON = EmissionFactor(
        name="Cotton",
        factor=Decimal("5.89"),
        unit="kg CO2e/kg",
        source="Textile Exchange 2023",
        year=2023
    )
    CONCRETE = EmissionFactor(
        name="Concrete",
        factor=Decimal("0.13"),
        unit="kg CO2e/kg",
        source="DEFRA 2023",
        year=2023
    )


class TransportEmissionFactors(BaseModel):
    """Emission factors for transportation modes"""
    TRUCK_DIESEL = EmissionFactor(
        name="Truck (Diesel)",
        factor=Decimal("0.12"),
        unit="kg CO2e/km/tonne",
        source="DEFRA 2023",
        year=2023
    )
    RAIL_FREIGHT = EmissionFactor(
        name="Rail Freight",
        factor=Decimal("0.028"),
        unit="kg CO2e/km/tonne", 
        source="DEFRA 2023",
        year=2023
    )
    SHIP_CONTAINER = EmissionFactor(
        name="Container Ship",
        factor=Decimal("0.011"),
        unit="kg CO2e/km/tonne",
        source="IMO 2021",
        year=2021
    )
    AIR_FREIGHT = EmissionFactor(
        name="Air Freight",
        factor=Decimal("0.602"),
        unit="kg CO2e/km/tonne",
        source="DEFRA 2023", 
        year=2023
    )


class ProcessEmissionFactors(BaseModel):
    """Emission factors for industrial processes"""
    ELECTRICITY_GRID_US = EmissionFactor(
        name="US Grid Electricity",
        factor=Decimal("0.386"),
        unit="kg CO2e/kWh",
        source="EPA eGRID 2022",
        region="United States",
        year=2022
    )
    NATURAL_GAS = EmissionFactor(
        name="Natural Gas Combustion",
        factor=Decimal("0.184"),
        unit="kg CO2e/kWh",
        source="EPA 2023",
        year=2023
    )
    WATER_TREATMENT = EmissionFactor(
        name="Water Treatment",
        factor=Decimal("0.000149"),
        unit="kg CO2e/liter",
        source="DEFRA 2023",
        year=2023
    )


class CarbonCalculator:
    """Carbon footprint calculation utilities"""
    
    @staticmethod
    def calculate_material_emissions(
        material: Material,
        quantity: Decimal,
        custom_factor: Optional[EmissionFactor] = None
    ) -> CarbonFootprint:
        """Calculate emissions for material production"""
        if custom_factor:
            factor = custom_factor.factor
            methodology = f"Custom factor: {custom_factor.source}"
            confidence = 1.0 - (custom_factor.uncertainty or 0.0)
        elif material.carbon_intensity:
            factor = material.carbon_intensity
            methodology = "Material-specific carbon intensity"
            confidence = 0.8
        else:
            # Use default factors based on material type
            factor = CarbonCalculator._get_default_material_factor(material.name)
            methodology = "Default emission factor"
            confidence = 0.6
        
        total_co2e = quantity * factor
        
        return CarbonFootprint(
            total_co2e=total_co2e,
            scope3=total_co2e,  # Material production is typically Scope 3
            methodology=methodology,
            confidence_level=confidence
        )
    
    @staticmethod
    def calculate_transport_emissions(
        transport_mode: TransportMode,
        distance_km: Decimal,
        weight_tonnes: Decimal
    ) -> CarbonFootprint:
        """Calculate transportation emissions"""
        factors = {
            TransportMode.TRUCK: TransportEmissionFactors.TRUCK_DIESEL,
            TransportMode.RAIL: TransportEmissionFactors.RAIL_FREIGHT,
            TransportMode.SHIP: TransportEmissionFactors.SHIP_CONTAINER,
            TransportMode.AIR: TransportEmissionFactors.AIR_FREIGHT
        }
        
        factor = factors.get(transport_mode, TransportEmissionFactors.TRUCK_DIESEL)
        total_co2e = distance_km * weight_tonnes * factor.factor
        
        return CarbonFootprint(
            total_co2e=total_co2e,
            scope3=total_co2e,  # Transportation is typically Scope 3
            methodology=f"Transport emission factor: {factor.source}",
            confidence_level=0.8
        )
    
    @staticmethod
    def calculate_process_emissions(
        process: Process,
        electricity_factor: Optional[EmissionFactor] = None
    ) -> CarbonFootprint:
        """Calculate process-specific emissions"""
        total_co2e = Decimal("0")
        breakdown = {}
        
        # Energy emissions
        if process.energy_consumption:
            energy_factor = electricity_factor or ProcessEmissionFactors.ELECTRICITY_GRID_US
            energy_emissions = process.energy_consumption * energy_factor.factor
            total_co2e += energy_emissions
            breakdown["energy"] = energy_emissions
        
        # Water emissions  
        if process.water_consumption:
            water_emissions = process.water_consumption * ProcessEmissionFactors.WATER_TREATMENT.factor
            total_co2e += water_emissions
            breakdown["water"] = water_emissions
        
        return CarbonFootprint(
            total_co2e=total_co2e,
            scope2=breakdown.get("energy", Decimal("0")),
            scope3=breakdown.get("water", Decimal("0")),
            methodology="Process-based calculation",
            confidence_level=0.7,
            breakdown=breakdown
        )
    
    @staticmethod
    def aggregate_carbon_footprints(footprints: List[CarbonFootprint]) -> CarbonFootprint:
        """Aggregate multiple carbon footprints"""
        total_co2e = sum(fp.total_co2e for fp in footprints)
        total_scope1 = sum(fp.scope1 or Decimal("0") for fp in footprints)
        total_scope2 = sum(fp.scope2 or Decimal("0") for fp in footprints)
        total_scope3 = sum(fp.scope3 or Decimal("0") for fp in footprints)
        
        # Weighted average confidence
        weighted_confidence = sum(
            fp.confidence_level * fp.total_co2e for fp in footprints
        ) / total_co2e if total_co2e > 0 else 0.0
        
        return CarbonFootprint(
            total_co2e=total_co2e,
            scope1=total_scope1 if total_scope1 > 0 else None,
            scope2=total_scope2 if total_scope2 > 0 else None,
            scope3=total_scope3 if total_scope3 > 0 else None,
            methodology="Aggregated calculation",
            confidence_level=weighted_confidence
        )
    
    @staticmethod
    def _get_default_material_factor(material_name: str) -> Decimal:
        """Get default emission factor for material"""
        material_lower = material_name.lower()
        
        if "steel" in material_lower:
            return MaterialEmissionFactors.STEEL.factor
        elif "aluminum" in material_lower or "aluminium" in material_lower:
            return MaterialEmissionFactors.ALUMINUM.factor
        elif "plastic" in material_lower or "pet" in material_lower:
            return MaterialEmissionFactors.PLASTIC_PET.factor
        elif "cotton" in material_lower:
            return MaterialEmissionFactors.COTTON.factor
        elif "concrete" in material_lower:
            return MaterialEmissionFactors.CONCRETE.factor
        else:
            # Generic manufacturing emission factor
            return Decimal("2.0")  # kg CO2e/kg