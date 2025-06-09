"""
Supply chain analysis service that coordinates AI analysis with business logic
"""
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import structlog

from ..core.config import Settings
from .ai_service import AIService
from .api_key_service import APIKeyService

logger = structlog.get_logger(__name__)


class AnalysisSession:
    """Represents an active analysis session"""
    
    def __init__(self, session_id: str, item_name: str, item_description: Optional[str] = None):
        self.session_id = session_id
        self.item_name = item_name
        self.item_description = item_description
        self.created_at = datetime.utcnow()
        self.status = "pending"  # pending, processing, completed, failed
        self.clarifications: Dict[str, Any] = {}
        self.analysis_result: Optional[Dict[str, Any]] = None
        self.progress_percentage = 0
        self.current_step = "Initializing"
        self.estimated_completion_time: Optional[datetime] = None


class AnalysisService:
    """Service for managing supply chain analysis sessions"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.api_key_service = APIKeyService(settings)
        self.ai_service = AIService(settings, self.api_key_service)
        # In-memory storage for now - would use Redis/database in production
        self.sessions: Dict[str, AnalysisSession] = {}
    
    def set_api_keys(self, session_id: str, api_keys: Dict[str, str]):
        """Set user-provided API keys for a session"""
        self.api_key_service.set_user_api_keys(session_id, api_keys)
    
    def get_available_services(self, session_id: Optional[str] = None) -> Dict[str, bool]:
        """Get which AI services are available for a session"""
        return self.api_key_service.get_available_services(session_id)
    
    async def start_analysis(
        self, 
        item_name: str, 
        item_description: Optional[str] = None,
        quantity: int = 1
    ) -> Dict[str, Any]:
        """
        Start a new supply chain analysis
        
        Returns:
            Dictionary with session_id and clarification questions
        """
        # Create new session
        session_id = str(uuid.uuid4())
        session = AnalysisSession(session_id, item_name, item_description)
        self.sessions[session_id] = session
        
        logger.info("Started new analysis session", 
                   session_id=session_id, item_name=item_name)
        
        # Generate clarification questions
        clarifications = await self.ai_service.generate_clarification_questions(
            item_name
        )
        
        # Set estimated completion time
        session.estimated_completion_time = datetime.utcnow() + timedelta(seconds=30)
        
        return {
            "session_id": session_id,
            "clarifications": clarifications,
            "message": "Please provide clarifications to proceed with analysis"
        }
    
    async def submit_clarifications(
        self, 
        session_id: str, 
        clarifications: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Submit clarification responses and start analysis
        
        Args:
            session_id: The analysis session ID
            clarifications: List of clarification responses
            
        Returns:
            Dictionary with status and estimated completion time
        """
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Store clarifications
        for clarification in clarifications:
            session.clarifications[clarification["question_id"]] = clarification["answer"]
        
        # Update session status
        session.status = "processing"
        session.progress_percentage = 10
        session.current_step = "Processing clarifications"
        
        logger.info("Clarifications submitted", 
                   session_id=session_id, 
                   clarification_count=len(clarifications))
        
        # Start async analysis (in production, this would be a background task)
        await self._perform_analysis(session)
        
        return {
            "session_id": session_id,
            "status": session.status,
            "estimated_completion_time": 30,  # seconds
            "message": "Analysis started. Please check status for updates."
        }
    
    async def get_analysis_status(self, session_id: str) -> Dict[str, Any]:
        """Get the status of an analysis session"""
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        return {
            "session_id": session_id,
            "status": session.status,
            "progress_percentage": session.progress_percentage,
            "current_step": session.current_step,
            "estimated_time_remaining": self._calculate_time_remaining(session),
            "message": self._get_status_message(session)
        }
    
    async def get_analysis_result(self, session_id: str) -> Dict[str, Any]:
        """Get the completed analysis results"""
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        if session.status != "completed":
            raise ValueError(f"Analysis not completed. Current status: {session.status}")
        
        if not session.analysis_result:
            raise ValueError("Analysis result not available")
        
        # Return the full analysis result
        return {
            "session_id": session_id,
            "item_name": session.item_name,
            "analysis_result": session.analysis_result,
            "created_at": session.created_at.isoformat(),
            "clarifications_used": session.clarifications
        }
    
    async def _perform_analysis(self, session: AnalysisSession):
        """Perform the actual AI analysis"""
        try:
            # Update progress
            session.progress_percentage = 25
            session.current_step = "Analyzing supply chain"
            
            # Extract quantity from clarifications, defaulting to 1
            quantity = 1
            if "quantity" in session.clarifications:
                try:
                    quantity = int(session.clarifications["quantity"])
                except (ValueError, TypeError):
                    quantity = 1
            
            # Perform AI analysis
            analysis_result = await self.ai_service.analyze_supply_chain(
                item_name=session.item_name,
                item_description=session.item_description,
                quantity=quantity,
                clarifications=session.clarifications,
                session_id=session.session_id
            )
            
            # Update progress
            session.progress_percentage = 75
            session.current_step = "Calculating carbon footprint"
            
            # Enhance analysis with additional processing
            enhanced_result = await self._enhance_analysis_result(analysis_result, session)
            
            # Complete analysis
            session.analysis_result = enhanced_result
            session.status = "completed"
            session.progress_percentage = 100
            session.current_step = "Analysis complete"
            
            logger.info("Analysis completed successfully", session_id=session.session_id)
            
        except Exception as e:
            logger.error("Analysis failed", session_id=session.session_id, error=str(e))
            session.status = "failed"
            session.current_step = f"Analysis failed: {str(e)}"
    
    async def _enhance_analysis_result(
        self, 
        analysis_result: Dict[str, Any], 
        session: AnalysisSession
    ) -> Dict[str, Any]:
        """Enhance the AI analysis result with additional processing"""
        
        # Add session metadata
        enhanced_result = {
            **analysis_result,
            "session_metadata": {
                "session_id": session.session_id,
                "item_name": session.item_name,
                "item_description": session.item_description,
                "analysis_date": datetime.utcnow().isoformat(),
                "clarifications_used": session.clarifications
            }
        }
        
        # Add key insights based on the analysis
        insights = self._generate_key_insights(analysis_result)
        enhanced_result["key_insights"] = insights
        
        # Add recommendations
        recommendations = self._generate_recommendations(analysis_result)
        enhanced_result["recommendations"] = recommendations
        
        # Add data quality assessment
        enhanced_result["data_quality"] = {
            "confidence_level": "medium",  # TODO: Calculate based on data availability
            "limitations": [
                "Analysis based on typical industry patterns",
                "Actual values may vary by specific supplier and location",
                "Carbon calculations use average emission factors"
            ]
        }
        
        return enhanced_result
    
    def _generate_key_insights(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate key insights from the analysis"""
        insights = []
        
        env_impact = analysis_result.get("environmental_impact", {})
        total_carbon = env_impact.get("total_carbon_footprint_kg", 0)
        highest_impact = env_impact.get("highest_impact_stage", "unknown")
        
        if total_carbon > 0:
            insights.append(f"Total carbon footprint: {total_carbon:.1f} kg CO2e")
        
        if highest_impact != "unknown":
            insights.append(f"Highest environmental impact stage: {highest_impact}")
        
        materials = analysis_result.get("materials", [])
        high_carbon_materials = [m for m in materials if m.get("carbon_intensity") == "high"]
        if high_carbon_materials:
            insights.append(f"High carbon intensity materials identified: {len(high_carbon_materials)} materials")
        
        return insights
    
    def _generate_recommendations(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on the analysis"""
        recommendations = []
        
        # Use AI-generated improvement opportunities if available
        env_impact = analysis_result.get("environmental_impact", {})
        ai_opportunities = env_impact.get("improvement_opportunities", [])
        recommendations.extend(ai_opportunities)
        
        # Add generic recommendations based on analysis patterns
        materials = analysis_result.get("materials", [])
        if any(m.get("carbon_intensity") == "high" for m in materials):
            recommendations.append("Consider alternative materials with lower carbon intensity")
        
        transportation = analysis_result.get("transportation", [])
        if any(t.get("mode") == "air" for t in transportation):
            recommendations.append("Explore surface transportation options to reduce emissions")
        
        return recommendations
    
    def _calculate_time_remaining(self, session: AnalysisSession) -> Optional[int]:
        """Calculate estimated time remaining for analysis"""
        if session.status == "completed":
            return 0
        if session.status == "failed":
            return None
        
        # Simple estimation based on progress
        if session.progress_percentage >= 90:
            return 5
        elif session.progress_percentage >= 50:
            return 15
        else:
            return 25
    
    def _get_status_message(self, session: AnalysisSession) -> str:
        """Get a user-friendly status message"""
        status_messages = {
            "pending": "Analysis is queued and will start shortly",
            "processing": f"Analysis in progress: {session.current_step}",
            "completed": "Analysis completed successfully",
            "failed": f"Analysis failed: {session.current_step}"
        }
        return status_messages.get(session.status, "Unknown status")