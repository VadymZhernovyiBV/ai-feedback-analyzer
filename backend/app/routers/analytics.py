"""Analytics endpoints for feedback statistics."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from datetime import datetime, timedelta
from typing import Dict, List, Any

from app.database import get_async_session
from app.models.feedback import FeedbackEntry
from app.models.schemas import StatsResponse

router = APIRouter(prefix="/api", tags=["analytics"])


@router.get("/stats", response_model=StatsResponse)
async def get_statistics(
    db: AsyncSession = Depends(get_async_session)
):
    """Get analytics statistics for feedback."""
    
    # Get total feedback count
    total_query = select(func.count()).select_from(FeedbackEntry)
    total_feedback = await db.scalar(total_query) or 0
    
    # Get sentiment distribution
    sentiment_query = select(
        FeedbackEntry.sentiment,
        func.count(FeedbackEntry.id).label('count')
    ).group_by(FeedbackEntry.sentiment)
    
    sentiment_result = await db.execute(sentiment_query)
    sentiment_rows = sentiment_result.all()
    
    sentiment_distribution = {
        "positive": 0,
        "neutral": 0,
        "negative": 0
    }
    
    for row in sentiment_rows:
        sentiment_distribution[row.sentiment] = row.count
    
    # Get top categories
    category_query = select(
        FeedbackEntry.category,
        func.count(FeedbackEntry.id).label('count'),
        func.avg(FeedbackEntry.category_confidence).label('avg_confidence')
    ).group_by(
        FeedbackEntry.category
    ).order_by(
        func.count(FeedbackEntry.id).desc()
    ).limit(10)
    
    category_result = await db.execute(category_query)
    category_rows = category_result.all()
    
    top_categories = [
        {
            "category": row.category,
            "count": row.count,
            "avg_confidence": round(row.avg_confidence, 2) if row.avg_confidence else 0
        }
        for row in category_rows
    ]
    
    # Get recent activity (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    # Daily feedback count for the last 7 days
    daily_query = select(
        func.date(FeedbackEntry.created_at).label('date'),
        func.count(FeedbackEntry.id).label('count')
    ).where(
        FeedbackEntry.created_at >= seven_days_ago
    ).group_by(
        func.date(FeedbackEntry.created_at)
    ).order_by(
        func.date(FeedbackEntry.created_at)
    )
    
    daily_result = await db.execute(daily_query)
    daily_rows = daily_result.all()
    
    recent_activity = {}
    for row in daily_rows:
        date_str = row.date.strftime('%Y-%m-%d') if hasattr(row.date, 'strftime') else str(row.date)
        recent_activity[date_str] = row.count
    
    # Fill in missing days with 0
    for i in range(7):
        date = (datetime.utcnow() - timedelta(days=i)).strftime('%Y-%m-%d')
        if date not in recent_activity:
            recent_activity[date] = 0
    
    # Get average confidence scores
    confidence_query = select(
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
    
    confidence_result = await db.execute(confidence_query)
    confidence_row = confidence_result.one()
    
    average_confidence = {
        "sentiment_positive": round(confidence_row.positive_confidence, 2) if confidence_row.positive_confidence else 0,
        "sentiment_neutral": round(confidence_row.neutral_confidence, 2) if confidence_row.neutral_confidence else 0,
        "sentiment_negative": round(confidence_row.negative_confidence, 2) if confidence_row.negative_confidence else 0,
        "category": round(confidence_row.category_confidence, 2) if confidence_row.category_confidence else 0
    }
    
    return StatsResponse(
        total_feedback=total_feedback,
        sentiment_distribution=sentiment_distribution,
        top_categories=top_categories,
        recent_activity=recent_activity,
        average_confidence=average_confidence
    )