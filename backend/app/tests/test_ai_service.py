"""Tests for AI service integration."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
import json

from app.services.ai_service import OpenRouterClient
from app.utils.exceptions import AIServiceError


@pytest.fixture
def mock_httpx_response():
    """Create a mock httpx response."""
    def _create_response(content, status_code=200):
        response = MagicMock()
        response.status_code = status_code
        response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps(content) if isinstance(content, dict) else content
                }
            }]
        }
        response.raise_for_status = MagicMock()
        if status_code >= 400:
            response.raise_for_status.side_effect = httpx.HTTPStatusError(
                message="Error",
                request=MagicMock(),
                response=MagicMock(status_code=status_code)
            )
        return response
    return _create_response


@pytest.mark.asyncio
async def test_analyze_feedback_success(mock_httpx_response):
    """Test successful feedback analysis."""
    sentiment_response = {
        "sentiment": "positive",
        "confidence": 0.95,
        "reasoning": "Positive language detected"
    }
    category_response = {
        "category": "Product Quality",
        "confidence": 0.88,
        "reasoning": "Mentions product features"
    }
    
    with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
        # Mock both API calls
        mock_post.side_effect = [
            mock_httpx_response(sentiment_response),
            mock_httpx_response(category_response)
        ]
        
        async with OpenRouterClient() as client:
            result = await client.analyze_feedback("Great product!")
        
        assert result["sentiment"] == "positive"
        assert result["sentiment_confidence"] == 0.95
        assert result["category"] == "Product Quality"
        assert result["category_confidence"] == 0.88
        assert result["model_used"] == "openai/gpt-3.5-turbo"


@pytest.mark.asyncio
async def test_analyze_feedback_fallback_to_free_model(mock_httpx_response):
    """Test fallback to free model when primary fails."""
    sentiment_response = {
        "sentiment": "negative",
        "confidence": 0.85,
        "reasoning": "Negative sentiment"
    }
    category_response = {
        "category": "Customer Service",
        "confidence": 0.75,
        "reasoning": "Service complaint"
    }
    
    with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
        # First two calls fail (primary model), next two succeed (free model)
        mock_post.side_effect = [
            httpx.HTTPStatusError(
                message="Rate limit",
                request=MagicMock(),
                response=MagicMock(status_code=429)
            ),
            httpx.HTTPStatusError(
                message="Rate limit",
                request=MagicMock(),
                response=MagicMock(status_code=429)
            ),
            mock_httpx_response(sentiment_response),
            mock_httpx_response(category_response)
        ]
        
        async with OpenRouterClient() as client:
            result = await client.analyze_feedback("Bad service!")
        
        assert result["sentiment"] == "negative"
        assert result["model_used"] == "meta-llama/llama-3.1-8b-instruct:free"


@pytest.mark.asyncio
async def test_analyze_feedback_all_models_fail():
    """Test when all models fail."""
    with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = httpx.HTTPStatusError(
            message="Service unavailable",
            request=MagicMock(),
            response=MagicMock(status_code=503)
        )
        
        async with OpenRouterClient() as client:
            with pytest.raises(AIServiceError) as exc_info:
                await client.analyze_feedback("Test feedback")
            
            assert "All models failed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_parse_json_response_valid():
    """Test parsing valid JSON response."""
    client = OpenRouterClient()
    
    # Direct JSON
    result = client._parse_json_response('{"key": "value"}')
    assert result == {"key": "value"}
    
    # JSON with extra text
    result = client._parse_json_response('Here is the result: {"key": "value"} Done.')
    assert result == {"key": "value"}
    
    # JSON in code block
    result = client._parse_json_response('```json\n{"key": "value"}\n```')
    assert result == {"key": "value"}


@pytest.mark.asyncio
async def test_parse_json_response_invalid():
    """Test parsing invalid JSON response."""
    client = OpenRouterClient()
    
    with pytest.raises(AIServiceError) as exc_info:
        client._parse_json_response("This is not JSON")
    
    assert "Invalid JSON response" in str(exc_info.value)


@pytest.mark.asyncio
async def test_check_health_success(mock_httpx_response):
    """Test health check when service is available."""
    with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MagicMock(status_code=200)
        
        async with OpenRouterClient() as client:
            health = await client.check_health()
        
        assert health is True


@pytest.mark.asyncio
async def test_check_health_failure():
    """Test health check when service is unavailable."""
    with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = httpx.RequestError("Connection failed")
        
        async with OpenRouterClient() as client:
            health = await client.check_health()
        
        assert health is False