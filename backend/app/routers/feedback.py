"""Feedback CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import List, Optional
import time
import logging

from app.database import get_async_session
from app.models.feedback import FeedbackEntry
from app.models.schemas import (
    FeedbackCreate, FeedbackResponse, FeedbackUpdate,
    PaginatedResponse, ErrorResponse
)
from app.services.ai_service import OpenRouterClient
from app.utils.exceptions import AIServiceError, NotFoundError
from app.utils.validators import validate_pagination, validate_sentiment

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("/analyze", response_model=FeedbackResponse)
async def analyze_feedback(
    feedback: FeedbackCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Analyze new feedback with AI."""
    # Record start time
    start_time = time.time()
    
    # Initialize AI client
    async with OpenRouterClient() as ai_client:
        try:
            # Get AI analysis
            logger.info(f"Analyzing feedback: {feedback.text[:100]}...")
            analysis = await ai_client.analyze_feedback(feedback.text)
            
            # Calculate duration
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Create database entry
            db_feedback = FeedbackEntry(
                text=feedback.text,
                sentiment=analysis["sentiment"],
                sentiment_confidence=analysis["sentiment_confidence"],
                category=analysis["category"],
                category_confidence=analysis["category_confidence"],
                tags=feedback.tags,
                analysis_duration_ms=duration_ms,
                model_used=analysis["model_used"]
            )
            
            db.add(db_feedback)
            await db.commit()
            await db.refresh(db_feedback)
            
            logger.info(f"Feedback analyzed successfully: ID={db_feedback.id}")
            return FeedbackResponse.model_validate(db_feedback)
            
        except AIServiceError as e:
            logger.error(f"AI service error: {str(e)}")
            await db.rollback()
            raise HTTPException(status_code=503, detail=str(e))
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            await db.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=PaginatedResponse[FeedbackResponse])
async def get_feedback_list(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sentiment: Optional[str] = Query(None, description="Filter by sentiment"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in feedback text"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    db: AsyncSession = Depends(get_async_session)
):
    """Get paginated feedback with filters."""
    # Validate pagination
    page, page_size = validate_pagination(page, page_size)
    
    # Build query
    query = select(FeedbackEntry)
    
    # Apply filters
    filters = []
    
    if sentiment:
        validated_sentiment = validate_sentiment(sentiment)
        if validated_sentiment:
            filters.append(FeedbackEntry.sentiment == validated_sentiment)
    
    if category:
        filters.append(FeedbackEntry.category.ilike(f"%{category}%"))
    
    if search:
        filters.append(FeedbackEntry.text.ilike(f"%{search}%"))
    
    if tag:
        # For SQLite, we need to use JSON extract
        filters.append(
            func.json_extract(FeedbackEntry.tags, '$').like(f'%"{tag}"%')
        )
    
    if filters:
        query = query.where(or_(*filters))
    
    # Order by created_at desc
    query = query.order_by(FeedbackEntry.created_at.desc())
    
    # Get total count
    count_query = select(func.count()).select_from(FeedbackEntry)
    if filters:
        count_query = count_query.where(or_(*filters))
    
    total = await db.scalar(count_query) or 0
    
    # Apply pagination
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    # Execute query
    result = await db.execute(query)
    items = result.scalars().all()
    
    return PaginatedResponse(
        items=[FeedbackResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size if total > 0 else 0
    )


@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(
    feedback_id: int = Path(..., description="Feedback ID"),
    db: AsyncSession = Depends(get_async_session)
):
    """Get specific feedback by ID."""
    query = select(FeedbackEntry).where(FeedbackEntry.id == feedback_id)
    result = await db.execute(query)
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    return FeedbackResponse.model_validate(feedback)


@router.put("/{feedback_id}/tags", response_model=FeedbackResponse)
async def update_feedback_tags(
    feedback_id: int = Path(..., description="Feedback ID"),
    update_data: FeedbackUpdate = ...,
    db: AsyncSession = Depends(get_async_session)
):
    """Update feedback tags."""
    # Get feedback
    query = select(FeedbackEntry).where(FeedbackEntry.id == feedback_id)
    result = await db.execute(query)
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # Update tags
    feedback.tags = update_data.tags
    
    await db.commit()
    await db.refresh(feedback)
    
    return FeedbackResponse.model_validate(feedback)


@router.delete("/{feedback_id}")
async def delete_feedback(
    feedback_id: int = Path(..., description="Feedback ID"),
    db: AsyncSession = Depends(get_async_session)
):
    """Delete feedback entry."""
    # Get feedback
    query = select(FeedbackEntry).where(FeedbackEntry.id == feedback_id)
    result = await db.execute(query)
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # Delete feedback
    await db.delete(feedback)
    await db.commit()
    
    return {"message": "Feedback deleted successfully"}