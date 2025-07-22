"""SQLAlchemy models for feedback entries."""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, Index
from sqlalchemy.sql import func

from app.database import Base


class FeedbackEntry(Base):
    """Model for storing feedback entries with AI analysis results."""
    
    __tablename__ = "feedback_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)  # Max 5000 chars enforced in API
    sentiment = Column(String(20), nullable=False)  # enum: positive/neutral/negative
    sentiment_confidence = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    category_confidence = Column(Float, nullable=False)
    tags = Column(JSON, default=list)  # JSON array of strings
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    analysis_duration_ms = Column(Integer, nullable=False)
    model_used = Column(String(50), nullable=False)
    
    # Add indexes for common query patterns
    __table_args__ = (
        Index('idx_sentiment', 'sentiment'),
        Index('idx_category', 'category'),
        Index('idx_created_at_desc', created_at.desc()),
    )