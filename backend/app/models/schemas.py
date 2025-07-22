"""Pydantic schemas for API request/response models."""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional, Generic, TypeVar, Any
from datetime import datetime
from enum import Enum


class SentimentEnum(str, Enum):
    """Valid sentiment values."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class FeedbackCreate(BaseModel):
    """Schema for creating new feedback."""
    text: str = Field(..., min_length=1, max_length=5000)
    tags: Optional[List[str]] = Field(default_factory=list)
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Ensure text is not empty after stripping."""
        if not v.strip():
            raise ValueError('Feedback text cannot be empty')
        return v.strip()
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: Optional[List[str]]) -> List[str]:
        """Validate and clean tags."""
        if v is None:
            return []
        # Remove empty tags and duplicates
        cleaned_tags = list(set(tag.strip() for tag in v if tag.strip()))
        return cleaned_tags[:10]  # Limit to 10 tags


class FeedbackResponse(BaseModel):
    """Schema for feedback response."""
    id: int
    text: str
    sentiment: SentimentEnum
    sentiment_confidence: float
    category: str
    category_confidence: float
    tags: List[str]
    created_at: datetime
    analysis_duration_ms: int
    model_used: str
    
    model_config = ConfigDict(
        from_attributes=True,
        protected_namespaces=()  # Disable protected namespace check
    )


class FeedbackUpdate(BaseModel):
    """Schema for updating feedback tags."""
    tags: List[str] = Field(..., max_length=10)
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        """Validate and clean tags."""
        cleaned_tags = list(set(tag.strip() for tag in v if tag.strip()))
        return cleaned_tags[:10]


class AnalysisResult(BaseModel):
    """Schema for AI analysis result."""
    sentiment: SentimentEnum
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    
    @field_validator('sentiment')
    @classmethod
    def validate_sentiment(cls, v: str) -> str:
        """Ensure sentiment is valid."""
        if v not in ['positive', 'neutral', 'negative']:
            raise ValueError('Invalid sentiment value')
        return v


class CategoryResult(BaseModel):
    """Schema for category analysis result."""
    category: str = Field(..., min_length=1, max_length=100)
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str


# Generic pagination response
T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int


class StatsResponse(BaseModel):
    """Schema for analytics statistics."""
    total_feedback: int
    sentiment_distribution: dict[str, int]
    top_categories: List[dict[str, Any]]
    recent_activity: dict[str, int]
    average_confidence: dict[str, float]


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str
    database: str
    ai_service: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str
    message: str
    details: Optional[dict] = None