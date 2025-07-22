"""Tests for feedback endpoints."""
import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient

from app.services.ai_service import OpenRouterClient


@pytest.mark.asyncio
async def test_analyze_feedback_success(client: AsyncClient, mock_ai_response):
    """Test successful feedback analysis."""
    # Mock the AI service
    with patch.object(OpenRouterClient, 'analyze_feedback', new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = mock_ai_response
        
        response = await client.post(
            "/api/feedback/analyze",
            json={
                "text": "This product is amazing! Great quality and fast shipping.",
                "tags": ["product", "shipping"]
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["sentiment"] == "positive"
    assert data["sentiment_confidence"] == 0.95
    assert data["category"] == "Product Quality"
    assert data["category_confidence"] == 0.88
    assert data["tags"] == ["product", "shipping"]
    assert "id" in data
    assert "created_at" in data
    assert "analysis_duration_ms" in data


@pytest.mark.asyncio
async def test_analyze_feedback_empty_text(client: AsyncClient):
    """Test feedback analysis with empty text."""
    response = await client.post(
        "/api/feedback/analyze",
        json={"text": "", "tags": []}
    )
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_analyze_feedback_long_text(client: AsyncClient):
    """Test feedback analysis with text exceeding limit."""
    long_text = "x" * 5001
    response = await client.post(
        "/api/feedback/analyze",
        json={"text": long_text, "tags": []}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_feedback_list_empty(client: AsyncClient):
    """Test getting feedback list when empty."""
    response = await client.get("/api/feedback/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["pages"] == 0


@pytest.mark.asyncio
async def test_get_feedback_list_with_data(client: AsyncClient, mock_ai_response):
    """Test getting feedback list with data."""
    # First, create some feedback
    with patch.object(OpenRouterClient, 'analyze_feedback', new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = mock_ai_response
        
        # Create 3 feedback entries
        for i in range(3):
            await client.post(
                "/api/feedback/analyze",
                json={
                    "text": f"Test feedback {i}",
                    "tags": [f"tag{i}"]
                }
            )
    
    # Get the list
    response = await client.get("/api/feedback/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["items"]) == 3
    assert data["total"] == 3
    assert data["pages"] == 1


@pytest.mark.asyncio
async def test_get_feedback_by_id(client: AsyncClient, mock_ai_response):
    """Test getting specific feedback by ID."""
    # Create feedback
    with patch.object(OpenRouterClient, 'analyze_feedback', new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = mock_ai_response
        
        create_response = await client.post(
            "/api/feedback/analyze",
            json={
                "text": "Test feedback",
                "tags": ["test"]
            }
        )
    
    feedback_id = create_response.json()["id"]
    
    # Get by ID
    response = await client.get(f"/api/feedback/{feedback_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == feedback_id
    assert data["text"] == "Test feedback"


@pytest.mark.asyncio
async def test_get_feedback_not_found(client: AsyncClient):
    """Test getting non-existent feedback."""
    response = await client.get("/api/feedback/99999")
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Feedback not found"


@pytest.mark.asyncio
async def test_update_feedback_tags(client: AsyncClient, mock_ai_response):
    """Test updating feedback tags."""
    # Create feedback
    with patch.object(OpenRouterClient, 'analyze_feedback', new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = mock_ai_response
        
        create_response = await client.post(
            "/api/feedback/analyze",
            json={
                "text": "Test feedback",
                "tags": ["old-tag"]
            }
        )
    
    feedback_id = create_response.json()["id"]
    
    # Update tags
    response = await client.put(
        f"/api/feedback/{feedback_id}/tags",
        json={"tags": ["new-tag1", "new-tag2"]}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == ["new-tag1", "new-tag2"]


@pytest.mark.asyncio
async def test_delete_feedback(client: AsyncClient, mock_ai_response):
    """Test deleting feedback."""
    # Create feedback
    with patch.object(OpenRouterClient, 'analyze_feedback', new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = mock_ai_response
        
        create_response = await client.post(
            "/api/feedback/analyze",
            json={
                "text": "Test feedback to delete",
                "tags": []
            }
        )
    
    feedback_id = create_response.json()["id"]
    
    # Delete feedback
    response = await client.delete(f"/api/feedback/{feedback_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Feedback deleted successfully"
    
    # Verify it's deleted
    get_response = await client.get(f"/api/feedback/{feedback_id}")
    assert get_response.status_code == 404