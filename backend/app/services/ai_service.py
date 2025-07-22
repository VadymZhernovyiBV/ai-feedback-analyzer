"""OpenRouter AI service for feedback analysis."""
import httpx
import json
import asyncio
from typing import Dict, Any, Optional
import logging
import re

from app.config import settings
from app.models.schemas import AnalysisResult, CategoryResult
from app.utils.exceptions import AIServiceError

logger = logging.getLogger(__name__)


class OpenRouterClient:
    """Client for OpenRouter API integration."""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        
    async def analyze_feedback(self, text: str) -> Dict[str, Any]:
        """Analyze feedback for sentiment and category."""
        # Try primary model first, fallback to free model
        models = [
            # "openai/gpt-3.5-turbo",
            "qwen/qwen3-235b-a22b-07-25:free"
        ]
        
        last_error = None
        for model in models:
            try:
                # Run both analyses in parallel
                sentiment_task = asyncio.create_task(
                    self._analyze_sentiment(text, model)
                )
                category_task = asyncio.create_task(
                    self._categorize_feedback(text, model)
                )
                
                sentiment_result, category_result = await asyncio.gather(
                    sentiment_task, category_task
                )
                
                return {
                    "sentiment": sentiment_result["sentiment"],
                    "sentiment_confidence": sentiment_result["confidence"],
                    "category": category_result["category"],
                    "category_confidence": category_result["confidence"],
                    "model_used": model
                }
            except Exception as e:
                logger.warning(f"Model {model} failed: {str(e)}")
                last_error = e
                if model == models[-1]:  # Last model
                    raise AIServiceError(
                        f"All models failed. Last error: {str(last_error)}"
                    )
                continue
    
    async def _analyze_sentiment(self, text: str, model: str) -> Dict[str, Any]:
        """Analyze sentiment of the feedback text."""
        prompt = f"""Analyze the sentiment of the following customer feedback text. 
Respond with ONLY a JSON object in this exact format:
{{
    "sentiment": "positive" or "neutral" or "negative",
    "confidence": 0.0 to 1.0,
    "reasoning": "brief explanation"
}}

Customer feedback: "{text}" """
        
        result = await self._make_request(prompt, model)
        # Validate result
        AnalysisResult.model_validate(result)
        return result
    
    async def _categorize_feedback(self, text: str, model: str) -> Dict[str, Any]:
        """Categorize the feedback text."""
        prompt = f"""Categorize the following customer feedback into one main category.
Choose from common categories like: Product Quality, Customer Service, Delivery, 
Pricing, User Experience, Technical Issues, Feature Request, or create a new specific category if needed.

Respond with ONLY a JSON object in this exact format:
{{
    "category": "Category Name",
    "confidence": 0.0 to 1.0,
    "reasoning": "brief explanation"
}}

Customer feedback: "{text}" """
        
        result = await self._make_request(prompt, model)
        # Validate result
        CategoryResult.model_validate(result)
        return result
    
    async def _make_request(self, prompt: str, model: str) -> Dict[str, Any]:
        """Make request to OpenRouter API."""
        # CRITICAL: Required headers for OpenRouter
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": settings.APP_URL or "http://localhost:8000",
            "X-Title": "AI Feedback Analyzer"
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an expert at analyzing customer feedback. Always respond with valid JSON only, no additional text."
                },
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 200,
            "temperature": 0.3,  # Low for consistency
            "stream": False  # MUST be False
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            
            # Parse response and extract JSON
            result = response.json()
            
            if "choices" not in result or len(result["choices"]) == 0:
                raise AIServiceError("Invalid response from AI service")
                
            content = result["choices"][0]["message"]["content"]
            
            # CRITICAL: Safely parse JSON response
            return self._parse_json_response(content)
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise AIServiceError("Rate limit exceeded. Please try again later.")
            elif e.response.status_code == 401:
                raise AIServiceError("Invalid API key")
            else:
                raise AIServiceError(f"AI service error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise AIServiceError(f"Network error: {str(e)}")
    
    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """Safely parse JSON from AI response."""
        try:
            # First try direct JSON parsing
            return json.loads(content)
        except json.JSONDecodeError:
            # Extract JSON from response if wrapped in text
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            
            # Try to find JSON between code blocks
            code_block_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
            if code_block_match:
                try:
                    return json.loads(code_block_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            raise AIServiceError(f"Invalid JSON response from AI: {content[:200]}...")
    
    async def check_health(self) -> bool:
        """Check if AI service is available."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            response = await self.client.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=5.0
            )
            return response.status_code == 200
        except Exception:
            return False