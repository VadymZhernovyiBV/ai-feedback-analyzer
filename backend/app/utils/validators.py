"""Input validation utilities."""
from typing import List, Optional
import re


def validate_feedback_text(text: str) -> str:
    """Validate and clean feedback text."""
    if not text or not text.strip():
        raise ValueError("Feedback text cannot be empty")
    
    cleaned_text = text.strip()
    
    if len(cleaned_text) > 5000:
        raise ValueError("Feedback text cannot exceed 5000 characters")
    
    # Remove excessive whitespace
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    return cleaned_text


def validate_tags(tags: Optional[List[str]]) -> List[str]:
    """Validate and clean tags list."""
    if not tags:
        return []
    
    cleaned_tags = []
    for tag in tags:
        if not isinstance(tag, str):
            continue
        
        cleaned_tag = tag.strip()
        if cleaned_tag and len(cleaned_tag) <= 50:
            cleaned_tags.append(cleaned_tag)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_tags = []
    for tag in cleaned_tags:
        if tag.lower() not in seen:
            seen.add(tag.lower())
            unique_tags.append(tag)
    
    return unique_tags[:10]  # Limit to 10 tags


def validate_pagination(page: int, page_size: int) -> tuple[int, int]:
    """Validate pagination parameters."""
    if page < 1:
        page = 1
    
    if page_size < 1:
        page_size = 20
    elif page_size > 100:
        page_size = 100
    
    return page, page_size


def validate_sentiment(sentiment: Optional[str]) -> Optional[str]:
    """Validate sentiment filter value."""
    if not sentiment:
        return None
    
    valid_sentiments = ["positive", "neutral", "negative"]
    if sentiment.lower() in valid_sentiments:
        return sentiment.lower()
    
    return None