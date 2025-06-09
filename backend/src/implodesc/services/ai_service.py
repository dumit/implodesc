"""
AI service for supply chain analysis using OpenAI and Anthropic
"""
import json
from typing import Dict, List, Optional, Any
import structlog
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from ..core.config import Settings
from .api_key_service import APIKeyService

logger = structlog.get_logger(__name__)


class AIService:
    """Service for AI-powered supply chain analysis"""
    
    def __init__(self, settings: Settings, api_key_service: APIKeyService):
        self.settings = settings
        self.api_key_service = api_key_service
        self._openai_client = None
        self._anthropic_client = None
        
    async def _get_openai_client(self, session_id: Optional[str] = None) -> Optional[AsyncOpenAI]:
        """Get OpenAI client if API key is available"""
        api_key = self.api_key_service.get_openai_api_key(session_id)
        if not api_key:
            return None
        # Create new client for each session to handle different keys
        return AsyncOpenAI(api_key=api_key)
    
    async def _get_anthropic_client(self, session_id: Optional[str] = None) -> Optional[AsyncAnthropic]:
        """Get Anthropic client if API key is available"""
        api_key = self.api_key_service.get_anthropic_api_key(session_id)
        if not api_key:
            return None
        # Create new client for each session to handle different keys
        return AsyncAnthropic(api_key=api_key)

    async def analyze_supply_chain(
        self, 
        item_name: str, 
        item_description: Optional[str] = None,
        quantity: int = 1,
        clarifications: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform AI-powered supply chain analysis
        
        Args:
            item_name: Name of the product to analyze
            item_description: Optional description
            quantity: Quantity being analyzed
            clarifications: User-provided clarifications
            
        Returns:
            Dictionary containing supply chain analysis
        """
        logger.info("Starting AI supply chain analysis", 
                   item_name=item_name, quantity=quantity)
        
        # Build the analysis prompt
        prompt = self._build_analysis_prompt(
            item_name, item_description, quantity, clarifications
        )
        
        # Log the full prompt for debugging
        logger.info("Generated AI prompt", 
                   session_id=session_id,
                   prompt_length=len(prompt),
                   prompt_preview=prompt[:200] + "..." if len(prompt) > 200 else prompt)
        
        try:
            # Try OpenAI first, fallback to Anthropic
            openai_client = await self._get_openai_client(session_id)
            if openai_client:
                logger.info("Using OpenAI for analysis", session_id=session_id)
                return await self._analyze_with_openai(openai_client, prompt, session_id)
            
            anthropic_client = await self._get_anthropic_client(session_id)
            if anthropic_client:
                logger.info("Using Anthropic for analysis", session_id=session_id)
                return await self._analyze_with_anthropic(anthropic_client, prompt)
            
            # No AI service available, return structured mock data
            logger.warning("No AI API keys available, returning enhanced mock data", 
                         session_id=session_id)
            return self._generate_enhanced_mock_analysis(item_name, quantity)
            
        except Exception as e:
            logger.error("AI analysis failed", error=str(e))
            # Fallback to enhanced mock data
            return self._generate_enhanced_mock_analysis(item_name, quantity)

    def _build_analysis_prompt(
        self, 
        item_name: str, 
        description: Optional[str],
        quantity: int,
        clarifications: Optional[Dict[str, Any]]
    ) -> str:
        """Build the prompt for AI analysis"""
        
        prompt = f"""
Analyze the supply chain for: {item_name}

Please provide a comprehensive supply chain analysis including:

1. **Materials Analysis**:
   - Primary raw materials and their sources
   - Key components and sub-assemblies
   - Material extraction and processing steps

2. **Manufacturing Process**:
   - Main manufacturing steps and processes
   - Energy requirements and types
   - Typical manufacturing locations/regions

3. **Transportation & Logistics**:
   - Transportation modes between stages
   - Typical distances and routes
   - Packaging requirements

4. **Key Companies & Suppliers**:
   - Major manufacturers in this industry
   - Key supplier regions
   - Notable supply chain risks

5. **Environmental Impact Factors**:
   - High carbon-intensity processes
   - Material extraction impacts
   - Transportation emissions
   - End-of-life considerations

Product Details:
- Item: {item_name}
- Quantity: {quantity}
"""
        
        if description:
            prompt += f"- Description: {description}\n"
            
        if clarifications:
            prompt += "\nUser Clarifications:\n"
            for key, value in clarifications.items():
                prompt += f"- {key}: {value}\n"
        
        prompt += """
Please respond in JSON format with the following structure:
{
  "materials": [
    {
      "name": "material name",
      "type": "raw_material|component|assembly",
      "source_regions": ["region1", "region2"],
      "carbon_intensity": "low|medium|high"
    }
  ],
  "processes": [
    {
      "name": "process name",
      "type": "extraction|processing|manufacturing|assembly",
      "energy_requirement": "energy amount and type",
      "location": "typical location",
      "carbon_emissions": "estimated CO2 kg"
    }
  ],
  "transportation": [
    {
      "from": "source",
      "to": "destination", 
      "mode": "truck|ship|air|rail",
      "distance_km": 1000,
      "carbon_emissions": "estimated CO2 kg"
    }
  ],
  "companies": [
    {
      "name": "company name",
      "role": "manufacturer|supplier|distributor",
      "region": "primary region"
    }
  ],
  "environmental_impact": {
    "total_carbon_footprint_kg": 0.0,
    "highest_impact_stage": "stage name",
    "improvement_opportunities": ["opportunity1", "opportunity2"]
  },
  "summary": "Brief summary of the supply chain analysis"
}
"""
        return prompt

    async def _analyze_with_openai(self, client: AsyncOpenAI, prompt: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Perform analysis using OpenAI"""
        logger.info("Using OpenAI for analysis")
        
        response = await client.chat.completions.create(
            model=self.settings.default_ai_model,
            messages=[
                {"role": "system", "content": "You are a supply chain expert providing detailed analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.settings.ai_max_tokens,
            temperature=self.settings.ai_temperature
        )
        
        content = response.choices[0].message.content
        try:
            # First try to parse as direct JSON
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code block
            try:
                import re
                json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
                if json_match:
                    json_content = json_match.group(1)
                    parsed_data = json.loads(json_content)
                    logger.info("Successfully extracted JSON from markdown", session_id=session_id)
                    return parsed_data
            except json.JSONDecodeError:
                pass
            
            # If all JSON parsing fails, wrap in basic structure
            logger.warning("Failed to parse JSON response, using fallback", session_id=session_id)
            return {
                "summary": content,
                "materials": [],
                "processes": [],
                "transportation": [],
                "companies": [],
                "environmental_impact": {
                    "total_carbon_footprint_kg": 0.0,
                    "highest_impact_stage": "unknown",
                    "improvement_opportunities": []
                }
            }

    async def _analyze_with_anthropic(self, client: AsyncAnthropic, prompt: str) -> Dict[str, Any]:
        """Perform analysis using Anthropic Claude"""
        logger.info("Using Anthropic Claude for analysis")
        
        response = await client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=self.settings.ai_max_tokens,
            temperature=self.settings.ai_temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "summary": content,
                "materials": [],
                "processes": [],
                "transportation": [],
                "companies": [],
                "environmental_impact": {
                    "total_carbon_footprint_kg": 0.0,
                    "highest_impact_stage": "unknown", 
                    "improvement_opportunities": []
                }
            }

    def _generate_enhanced_mock_analysis(self, item_name: str, quantity: int) -> Dict[str, Any]:
        """Generate realistic mock data when AI is not available"""
        logger.info("Generating enhanced mock analysis")
        
        # Basic analysis based on common product patterns
        if "cotton" in item_name.lower() or "t-shirt" in item_name.lower():
            return {
                "materials": [
                    {
                        "name": "Cotton fiber",
                        "type": "raw_material",
                        "source_regions": ["India", "China", "USA", "Brazil"],
                        "carbon_intensity": "medium"
                    },
                    {
                        "name": "Polyester thread",
                        "type": "component",
                        "source_regions": ["China", "India"],
                        "carbon_intensity": "high"
                    }
                ],
                "processes": [
                    {
                        "name": "Cotton cultivation",
                        "type": "extraction",
                        "energy_requirement": "Solar energy, irrigation",
                        "location": "Cotton growing regions",
                        "carbon_emissions": "2.1"
                    },
                    {
                        "name": "Textile manufacturing",
                        "type": "manufacturing",
                        "energy_requirement": "Grid electricity, natural gas",
                        "location": "China, Bangladesh, Vietnam",
                        "carbon_emissions": "3.8"
                    }
                ],
                "transportation": [
                    {
                        "from": "Cotton farm",
                        "to": "Textile mill",
                        "mode": "truck",
                        "distance_km": 500,
                        "carbon_emissions": "0.3"
                    },
                    {
                        "from": "Textile mill",
                        "to": "Distribution center",
                        "mode": "ship",
                        "distance_km": 8000,
                        "carbon_emissions": "0.8"
                    }
                ],
                "companies": [
                    {
                        "name": "H&M",
                        "role": "manufacturer",
                        "region": "Global"
                    },
                    {
                        "name": "Bangladesh textile mills",
                        "role": "supplier",
                        "region": "Bangladesh"
                    }
                ],
                "environmental_impact": {
                    "total_carbon_footprint_kg": 7.0 * int(quantity),
                    "highest_impact_stage": "Textile manufacturing",
                    "improvement_opportunities": [
                        "Use organic cotton",
                        "Renewable energy in manufacturing",
                        "Local sourcing to reduce transportation"
                    ]
                },
                "summary": f"The supply chain for {item_name} involves cotton cultivation, textile processing, and global distribution. The highest environmental impact comes from energy-intensive textile manufacturing processes."
            }
        
        # Generic product analysis
        return {
            "materials": [
                {
                    "name": "Primary material",
                    "type": "raw_material", 
                    "source_regions": ["China", "USA", "Germany"],
                    "carbon_intensity": "medium"
                }
            ],
            "processes": [
                {
                    "name": "Manufacturing",
                    "type": "manufacturing",
                    "energy_requirement": "Grid electricity",
                    "location": "Industrial regions",
                    "carbon_emissions": "5.0"
                }
            ],
            "transportation": [
                {
                    "from": "Factory",
                    "to": "Distribution",
                    "mode": "truck",
                    "distance_km": 1000,
                    "carbon_emissions": "1.2"
                }
            ],
            "companies": [
                {
                    "name": "Generic Manufacturer",
                    "role": "manufacturer",
                    "region": "Asia"
                }
            ],
            "environmental_impact": {
                "total_carbon_footprint_kg": 6.2 * int(quantity),
                "highest_impact_stage": "Manufacturing",
                "improvement_opportunities": [
                    "Improve energy efficiency",
                    "Use renewable energy",
                    "Optimize logistics"
                ]
            },
            "summary": f"Supply chain analysis for {item_name} shows typical manufacturing and distribution patterns with opportunities for carbon reduction."
        }

    async def generate_clarification_questions(
        self, 
        item_name: str, 
        initial_analysis: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Generate intelligent clarification questions based on item analysis"""
        
        # For now, return context-aware mock questions
        # TODO: Use AI to generate these based on initial analysis
        
        base_questions = [
            {
                "id": "use_case",
                "question": f"What is the intended use case for this {item_name}?",
                "type": "use_case",
                "options": ["Personal use", "Commercial use", "Industrial use", "Export/Wholesale"],
                "required": True
            },
            {
                "id": "quantity",
                "question": "What quantity are you analyzing?",
                "type": "quantity",
                "required": True
            },
            {
                "id": "quality",
                "question": "Do you have specific quality or material requirements?",
                "type": "specification",
                "required": False
            }
        ]
        
        # Add item-specific questions
        if "clothing" in item_name.lower() or "shirt" in item_name.lower():
            base_questions.append({
                "id": "material_preference",
                "question": "Do you have a preference for material type?",
                "type": "material",
                "options": ["Organic cotton", "Conventional cotton", "Polyester blend", "No preference"],
                "required": False
            })
            
        if "electronic" in item_name.lower() or "phone" in item_name.lower():
            base_questions.append({
                "id": "lifecycle",
                "question": "How long do you typically use this type of product?",
                "type": "lifecycle", 
                "options": ["1-2 years", "3-5 years", "5+ years"],
                "required": False
            })
        
        return base_questions