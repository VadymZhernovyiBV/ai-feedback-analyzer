"""Feedback service combining AI analysis with database operations."""
import logging
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.feedback import FeedbackEntry
from app.models.schemas import FeedbackCreate, FeedbackResponse
from app.services.ai_service import OpenRouterClient
from app.utils.exceptions import AIServiceError, NotFoundError

logger = logging.getLogger(__name__)


class FeedbackService:
    """Service for managing feedback operations."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.ai_client = OpenRouterClient()
    
    async def analyze_and_save_feedback(
        self,
        feedback_data: FeedbackCreate,
        start_time: float,
        end_time: float
    ) -> FeedbackResponse:
        """Analyze feedback with AI and save to database."""
        try:
            # Get AI analysis
            async with self.ai_client as client:
                analysis = await client.analyze_feedback(feedback_data.text)
            
            # Calculate duration
            duration_ms = int((end_time - start_time) * 1000)
            
            # Create database entry
            db_feedback = FeedbackEntry(
                text=feedback_data.text,
                sentiment=analysis["sentiment"],
                sentiment_confidence=analysis["sentiment_confidence"],
                category=analysis["category"],
                category_confidence=analysis["category_confidence"],
                tags=feedback_data.tags,
                analysis_duration_ms=duration_ms,
                model_used=analysis["model_used"]
            )
            
            self.db.add(db_feedback)
            await self.db.commit()
            await self.db.refresh(db_feedback)
            
            logger.info(
                f"Feedback analyzed and saved: ID={db_feedback.id}, "
                f"sentiment={db_feedback.sentiment}, category={db_feedback.category}"
            )
            
            return FeedbackResponse.model_validate(db_feedback)
            
        except AIServiceError:
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error analyzing feedback: {str(e)}")
            raise
    
    async def get_feedback_by_id(self, feedback_id: int) -> Optional[FeedbackEntry]:
        """Get feedback by ID."""
        query = select(FeedbackEntry).where(FeedbackEntry.id == feedback_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_feedback_tags(
        self,
        feedback_id: int,
        tags: list[str]
    ) -> FeedbackEntry:
        """Update feedback tags."""
        feedback = await self.get_feedback_by_id(feedback_id)
        if not feedback:
            raise NotFoundError(f"Feedback with ID {feedback_id} not found")
        
        feedback.tags = tags
        await self.db.commit()
        await self.db.refresh(feedback)
        
        logger.info(f"Updated tags for feedback ID={feedback_id}")
        return feedback
    
    async def delete_feedback(self, feedback_id: int) -> bool:
        """Delete feedback by ID."""
        feedback = await self.get_feedback_by_id(feedback_id)
        if not feedback:
            raise NotFoundError(f"Feedback with ID {feedback_id} not found")
        
        await self.db.delete(feedback)
        await self.db.commit()
        
        logger.info(f"Deleted feedback ID={feedback_id}")
        return True