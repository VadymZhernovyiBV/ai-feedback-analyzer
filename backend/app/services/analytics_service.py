"""Analytics service for generating statistics."""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case

from app.models.feedback import FeedbackEntry

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for generating analytics and statistics."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def get_total_feedback_count(self) -> int:
        """Get total number of feedback entries."""
        query = select(func.count()).select_from(FeedbackEntry)
        result = await self.db.scalar(query)
        return result or 0
    
    async def get_sentiment_distribution(self) -> Dict[str, int]:
        """Get distribution of sentiments."""
        query = select(
            FeedbackEntry.sentiment,
            func.count(FeedbackEntry.id).label('count')
        ).group_by(FeedbackEntry.sentiment)
        
        result = await self.db.execute(query)
        rows = result.all()
        
        # Initialize with zeros
        distribution = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }
        
        # Update with actual counts
        for row in rows:
            if row.sentiment in distribution:
                distribution[row.sentiment] = row.count
        
        return distribution
    
    async def get_top_categories(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top categories by count."""
        query = select(
            FeedbackEntry.category,
            func.count(FeedbackEntry.id).label('count'),
            func.avg(FeedbackEntry.category_confidence).label('avg_confidence')
        ).group_by(
            FeedbackEntry.category
        ).order_by(
            func.count(FeedbackEntry.id).desc()
        ).limit(limit)
        
        result = await self.db.execute(query)
        rows = result.all()
        
        return [
            {
                "category": row.category,
                "count": row.count,
                "avg_confidence": round(row.avg_confidence, 2) if row.avg_confidence else 0
            }
            for row in rows
        ]
    
    async def get_recent_activity(self, days: int = 7) -> Dict[str, int]:
        """Get daily feedback count for recent days."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Query for daily counts
        query = select(
            func.date(FeedbackEntry.created_at).label('date'),
            func.count(FeedbackEntry.id).label('count')
        ).where(
            FeedbackEntry.created_at >= start_date
        ).group_by(
            func.date(FeedbackEntry.created_at)
        ).order_by(
            func.date(FeedbackEntry.created_at)
        )
        
        result = await self.db.execute(query)
        rows = result.all()
        
        # Create activity dict
        activity = {}
        for row in rows:
            # Handle different date formats
            if hasattr(row.date, 'strftime'):
                date_str = row.date.strftime('%Y-%m-%d')
            else:
                date_str = str(row.date)
            activity[date_str] = row.count
        
        # Fill in missing days with 0
        for i in range(days):
            date = (datetime.utcnow() - timedelta(days=i)).strftime('%Y-%m-%d')
            if date not in activity:
                activity[date] = 0
        
        return activity
    
    async def get_average_confidence_scores(self) -> Dict[str, float]:
        """Get average confidence scores by sentiment and overall category."""
        query = select(
            func.avg(
                case(
                    (FeedbackEntry.sentiment == 'positive', FeedbackEntry.sentiment_confidence),
                    else_=None
                )
            ).label('positive_confidence'),
            func.avg(
                case(
                    (FeedbackEntry.sentiment == 'neutral', FeedbackEntry.sentiment_confidence),
                    else_=None
                )
            ).label('neutral_confidence'),
            func.avg(
                case(
                    (FeedbackEntry.sentiment == 'negative', FeedbackEntry.sentiment_confidence),
                    else_=None
                )
            ).label('negative_confidence'),
            func.avg(FeedbackEntry.category_confidence).label('category_confidence')
        )
        
        result = await self.db.execute(query)
        row = result.one()
        
        return {
            "sentiment_positive": round(row.positive_confidence or 0, 2),
            "sentiment_neutral": round(row.neutral_confidence or 0, 2),
            "sentiment_negative": round(row.negative_confidence or 0, 2),
            "category": round(row.category_confidence or 0, 2)
        }