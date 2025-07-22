name: "AI Feedback Analyzer - Full Stack Implementation"
description: |

## Purpose
Build a production-ready web application for AI-powered customer feedback analysis with sentiment classification, dynamic categorization, and comprehensive analytics dashboard.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## Goal
Create a full-stack web application that analyzes customer feedback using AI to determine sentiment (positive/neutral/negative) and categorize feedback dynamically. Users can submit feedback, view analysis results instantly, manage feedback history with filtering/sorting, and access analytics dashboards.

## Why
- **Business value**: Automate feedback analysis to understand customer sentiment at scale
- **User impact**: Instant insights into customer feedback without manual review
- **Integration**: Standalone application that can be embedded or API-accessed
- **Problems solved**: Manual feedback categorization is time-consuming and inconsistent

## What
### User-visible behavior:
- Submit feedback text (up to 5000 characters)
- See instant AI analysis with sentiment and category
- Browse feedback history with pagination
- Filter by sentiment, category, tags, and search text
- View analytics dashboard with charts
- Tag management for organizing feedback
- Anonymous usage (no authentication)

### Technical requirements:
- FastAPI backend with async operations
- React 19 + TypeScript frontend with Material-UI
- OpenRouter AI integration for analysis
- SQLite (dev) / PostgreSQL (prod) database
- Responsive design for mobile/desktop
- Free hosting on Vercel + Railway

### Success Criteria
- [ ] Feedback analysis completes in <2 seconds
- [ ] Frontend bundle size <500KB gzipped
- [ ] All API endpoints return proper error codes
- [ ] Mobile responsive design works on all devices
- [ ] Analytics dashboard updates in real-time
- [ ] Deployment successful on free tier hosting

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: https://openrouter.ai/docs
  why: API authentication, request format, rate limits
  critical: Must include HTTP-Referer and X-Title headers for free tier
  
- url: https://fastapi.tiangolo.com/tutorial/sql-databases/
  why: SQLAlchemy integration pattern with FastAPI
  section: "SQL (Relational) Databases"
  
- url: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
  why: ORM model definition and async session handling
  
- url: https://mui.com/material-ui/getting-started/
  why: Component library usage and theming
  
- url: https://redux-toolkit.js.org/tutorials/quick-start
  why: State management setup and slice patterns
  
- url: https://react-hook-form.com/get-started#SchemaValidation
  why: Form validation with Yup integration
  
- file: README.md
  why: Complete technical specification with API design, database schema, and architecture
  
- file: INITIAL.md
  why: Critical implementation details and common mistakes to avoid
```

### Current Codebase tree
```bash
.
├── INITIAL.md
├── PRPs/
│   └── templates/
│       └── prp_base.md
├── README.md
└── prompts/
    ├── 1-readme-project-specification.md
    ├── 2-project-ai-coding-rules.md
    ├── 3-generating-initial.md
    ├── 4-generate-prp.md
    └── 5-execute-prp.md
```

### Desired Codebase tree with files to be added
```bash
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── config.py              # Configuration and env vars
│   │   ├── database.py            # Database connection setup
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── feedback.py        # SQLAlchemy models
│   │   │   └── schemas.py         # Pydantic schemas
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── feedback.py        # Feedback CRUD endpoints
│   │   │   ├── analytics.py       # Stats endpoints
│   │   │   └── health.py          # Health check
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py      # OpenRouter integration
│   │   │   ├── feedback_service.py # Business logic
│   │   │   └── analytics_service.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── validators.py      # Input validation
│   │   │   ├── exceptions.py      # Custom exceptions
│   │   │   └── rate_limiter.py    # Rate limiting
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_feedback.py
│   │       ├── test_ai_service.py
│   │       └── conftest.py
│   ├── alembic/                    # Database migrations
│   │   └── versions/
│   ├── requirements.txt
│   ├── .env.example
│   ├── Dockerfile
│   └── railway.toml
└── frontend/
    ├── public/
    │   ├── index.html
    │   └── favicon.ico
    ├── src/
    │   ├── main.tsx               # App entry
    │   ├── App.tsx                # Root component
    │   ├── components/
    │   │   ├── common/
    │   │   │   ├── LoadingSpinner.tsx
    │   │   │   └── ErrorBoundary.tsx
    │   │   ├── feedback/
    │   │   │   ├── FeedbackForm.tsx
    │   │   │   ├── FeedbackCard.tsx
    │   │   │   └── FeedbackList.tsx
    │   │   └── layout/
    │   │       ├── Header.tsx
    │   │       └── Layout.tsx
    │   ├── pages/
    │   │   ├── HomePage.tsx
    │   │   ├── HistoryPage.tsx
    │   │   └── AnalyticsPage.tsx
    │   ├── store/
    │   │   ├── index.ts
    │   │   └── slices/
    │   │       └── feedbackSlice.ts
    │   ├── hooks/
    │   │   └── useDebounce.ts
    │   ├── utils/
    │   │   ├── api.ts
    │   │   └── constants.ts
    │   ├── types/
    │   │   └── feedback.ts
    │   └── styles/
    │       └── theme.ts
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    ├── .env.example
    └── vercel.json
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: OpenRouter requires specific headers
# Example: Must include HTTP-Referer and X-Title for free tier
headers = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "https://your-app.com",  # REQUIRED for free tier
    "X-Title": "AI Feedback Analyzer"        # REQUIRED for free tier
}

# CRITICAL: Don't use OpenAI SDK - use httpx for OpenRouter
# OpenRouter is OpenAI-compatible but needs httpx for custom headers

# CRITICAL: Set stream=False in OpenRouter requests
payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [...],
    "stream": False,  # MUST be False
    "temperature": 0.3  # Low temperature for consistent classification
}

# CRITICAL: Parse AI responses as JSON - validate before storage
# AI might return malformed JSON, always try/except json.loads()

# CRITICAL: Use proper async context managers with SQLAlchemy
# async with get_async_session() as session:
#     async with session.begin():
#         # operations here

# CRITICAL: Pydantic v2 syntax differs from v1
# Use model_validate() not parse_obj()
# Use model_dump() not dict()

# CRITICAL: CORS must be configured for production
# Only allow your Vercel frontend URL, not "*"

# CRITICAL: Railway free tier sleeps - implement wake strategy
# Add a scheduled ping or accept first request delay
```

## Implementation Blueprint

### Data models and structure

```python
# SQLAlchemy Models (app/models/feedback.py)
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class FeedbackEntry(Base):
    __tablename__ = "feedback_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)  # Max 5000 chars enforced in API
    sentiment = Column(String(20), nullable=False)  # enum: positive/neutral/negative
    sentiment_confidence = Column(Float)
    category = Column(String(100))
    category_confidence = Column(Float)
    tags = Column(JSON, default=list)  # JSON array of strings
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    analysis_duration_ms = Column(Integer)
    model_used = Column(String(50))

# Pydantic Schemas (app/models/schemas.py)
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    tags: Optional[List[str]] = Field(default_factory=list)
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Feedback text cannot be empty')
        return v.strip()

class FeedbackResponse(BaseModel):
    id: int
    text: str
    sentiment: str
    sentiment_confidence: float
    category: str
    category_confidence: float
    tags: List[str]
    created_at: datetime
    analysis_duration_ms: int
    model_used: str
    
    class Config:
        from_attributes = True  # Pydantic v2 syntax

class AnalysisResult(BaseModel):
    sentiment: str
    confidence: float
    reasoning: str
    
    @validator('sentiment')
    def validate_sentiment(cls, v):
        if v not in ['positive', 'neutral', 'negative']:
            raise ValueError('Invalid sentiment value')
        return v
```

### List of tasks to complete in order

```yaml
Task 1: Backend Foundation
CREATE backend/app/__init__.py:
  - Empty file for package initialization

CREATE backend/app/config.py:
  - Load environment variables with python-dotenv
  - Define settings class with all config values
  - Include OpenRouter API key, database URL, CORS origins
  - PATTERN: Use pydantic BaseSettings for validation

CREATE backend/app/database.py:
  - Setup async SQLAlchemy engine and sessionmaker
  - Create Base declarative class
  - Define get_async_session dependency
  - PATTERN: Use async context manager for sessions

CREATE backend/requirements.txt:
  - fastapi==0.104.1
  - uvicorn[standard]==0.24.0
  - sqlalchemy==2.0.23
  - asyncpg==0.29.0
  - alembic==1.12.1
  - pydantic==2.5.0
  - pydantic-settings==2.1.0
  - httpx==0.25.2
  - python-dotenv==1.0.0
  - python-multipart==0.0.6

Task 2: Database Models and Schemas
CREATE backend/app/models/__init__.py:
  - Import all models for Alembic detection

CREATE backend/app/models/feedback.py:
  - Define FeedbackEntry SQLAlchemy model
  - Include all fields from schema
  - Add indexes on created_at, sentiment, category

CREATE backend/app/models/schemas.py:
  - Define Pydantic models for API
  - FeedbackCreate, FeedbackResponse, FeedbackUpdate
  - AnalysisResult, StatsResponse
  - Use Pydantic v2 syntax

Task 3: Core Services
CREATE backend/app/services/__init__.py:
  - Empty file

CREATE backend/app/services/ai_service.py:
  - OpenRouterClient class with httpx
  - analyze_sentiment and categorize_feedback methods
  - Fallback logic for free models
  - CRITICAL: Include required headers
  - CRITICAL: Parse JSON responses safely

CREATE backend/app/utils/exceptions.py:
  - Define custom exceptions
  - APIError, ValidationError, AIServiceError
  - Consistent error response format

CREATE backend/app/utils/validators.py:
  - Text validation functions
  - Tag validation
  - Pagination parameter validation

Task 4: API Endpoints
CREATE backend/app/routers/__init__.py:
  - Import all routers

CREATE backend/app/routers/feedback.py:
  - POST /api/feedback/analyze endpoint
  - GET /api/feedback with pagination/filtering
  - GET /api/feedback/{id}
  - PUT /api/feedback/{id}/tags
  - DELETE /api/feedback/{id}
  - Use dependency injection for DB session

CREATE backend/app/routers/analytics.py:
  - GET /api/stats endpoint
  - Return sentiment distribution
  - Top categories
  - Recent activity metrics

CREATE backend/app/routers/health.py:
  - GET /api/health endpoint
  - Check database connection
  - Check AI service availability

CREATE backend/app/main.py:
  - FastAPI app initialization
  - CORS middleware configuration
  - Include all routers
  - Exception handlers
  - Startup/shutdown events

Task 5: Database Setup
CREATE backend/alembic.ini:
  - Alembic configuration
  - Point to app.database for models

CREATE backend/app/utils/init_db.py:
  - Create tables function
  - Initial migration generation

CREATE backend/.env.example:
  - OPENROUTER_API_KEY=
  - DATABASE_URL=sqlite+aiosqlite:///./feedback.db
  - CORS_ORIGINS=http://localhost:5173
  - LOG_LEVEL=INFO

Task 6: Backend Tests
CREATE backend/app/tests/conftest.py:
  - Pytest fixtures
  - Test database setup
  - Mock AI service

CREATE backend/app/tests/test_feedback.py:
  - Test all feedback endpoints
  - Test validation
  - Test error cases

CREATE backend/app/tests/test_ai_service.py:
  - Test AI integration
  - Test fallback logic
  - Test error handling

Task 7: Frontend Foundation
CREATE frontend/package.json:
  - React 18, TypeScript, Vite
  - Material-UI, Redux Toolkit
  - React Router, React Hook Form
  - All required dependencies

CREATE frontend/tsconfig.json:
  - TypeScript configuration
  - Strict mode enabled
  - Path aliases setup

CREATE frontend/vite.config.ts:
  - Vite configuration
  - Proxy for development API

CREATE frontend/index.html:
  - Basic HTML template
  - Meta tags for responsive

Task 8: Frontend Core Structure
CREATE frontend/src/main.tsx:
  - React 18 createRoot
  - Redux Provider setup
  - Material-UI ThemeProvider

CREATE frontend/src/App.tsx:
  - Router setup
  - Layout wrapper
  - Error boundary

CREATE frontend/src/types/feedback.ts:
  - TypeScript interfaces
  - Match backend schemas

CREATE frontend/src/utils/constants.ts:
  - API endpoints
  - App configuration
  - Sentiment colors

CREATE frontend/src/utils/api.ts:
  - Axios/fetch wrapper
  - Error handling
  - Request/response interceptors

Task 9: Redux Store Setup
CREATE frontend/src/store/index.ts:
  - Configure store with Redux Toolkit
  - Add middleware
  - Type exports

CREATE frontend/src/store/slices/feedbackSlice.ts:
  - Feedback state management
  - Async thunks for API calls
  - Reducers for CRUD operations

Task 10: Core Components
CREATE frontend/src/components/layout/Layout.tsx:
  - App layout wrapper
  - Header, main, footer

CREATE frontend/src/components/layout/Header.tsx:
  - App title and navigation
  - Responsive menu

CREATE frontend/src/components/common/LoadingSpinner.tsx:
  - Reusable loading component
  - Material-UI CircularProgress

CREATE frontend/src/components/common/ErrorBoundary.tsx:
  - Catch React errors
  - Fallback UI

Task 11: Feedback Components
CREATE frontend/src/components/feedback/FeedbackForm.tsx:
  - React Hook Form setup
  - Text area with character count
  - Tag input
  - Submit with loading state

CREATE frontend/src/components/feedback/FeedbackCard.tsx:
  - Display single feedback
  - Sentiment indicator
  - Tag display
  - Actions (edit tags, delete)

CREATE frontend/src/components/feedback/FeedbackList.tsx:
  - Map feedback entries
  - Empty state
  - Loading state

Task 12: Main Pages
CREATE frontend/src/pages/HomePage.tsx:
  - Feedback form
  - Recent submissions
  - Quick stats

CREATE frontend/src/pages/HistoryPage.tsx:
  - Filter panel
  - Paginated feedback list
  - Search functionality

CREATE frontend/src/pages/AnalyticsPage.tsx:
  - Stats cards
  - Sentiment pie chart
  - Category bar chart
  - Use recharts library

Task 13: Material-UI Theme
CREATE frontend/src/styles/theme.ts:
  - Custom MUI theme
  - Color palette
  - Typography settings
  - Component overrides

Task 14: Environment and Deployment
CREATE frontend/.env.example:
  - VITE_API_BASE_URL=http://localhost:8000

CREATE frontend/vercel.json:
  - SPA routing configuration
  - Environment variables

CREATE backend/Dockerfile:
  - Python 3.11 slim image
  - Install dependencies
  - Run uvicorn

CREATE backend/railway.toml:
  - Railway deployment config
  - Health check settings

Task 15: Final Integration
UPDATE backend/app/main.py:
  - Add rate limiting middleware
  - Configure production CORS

UPDATE frontend/src/utils/api.ts:
  - Use production API URL
  - Add request retry logic

CREATE backend/app/services/feedback_service.py:
  - Combine AI analysis with DB operations
  - Add caching layer
  - Transaction handling

CREATE frontend/src/hooks/useDebounce.ts:
  - Debounce search input
  - Optimize API calls
```

### Per task pseudocode

```python
# Task 3: AI Service Implementation
# backend/app/services/ai_service.py

import httpx
import json
from typing import Dict, Any, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class OpenRouterClient:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def analyze_feedback(self, text: str) -> Dict[str, Any]:
        """Analyze feedback for sentiment and category"""
        # Try primary model first, fallback to free model
        models = [
            "openai/gpt-3.5-turbo",
            "meta-llama/llama-3.1-8b-instruct:free"
        ]
        
        for model in models:
            try:
                # Run both analyses in parallel
                sentiment_task = self._analyze_sentiment(text, model)
                category_task = self._categorize_feedback(text, model)
                
                sentiment_result = await sentiment_task
                category_result = await category_task
                
                return {
                    "sentiment": sentiment_result["sentiment"],
                    "sentiment_confidence": sentiment_result["confidence"],
                    "category": category_result["category"],
                    "category_confidence": category_result["confidence"],
                    "model_used": model
                }
            except Exception as e:
                logger.warning(f"Model {model} failed: {e}")
                if model == models[-1]:  # Last model
                    raise
                continue
    
    async def _analyze_sentiment(self, text: str, model: str) -> Dict[str, Any]:
        prompt = f"""Analyze the sentiment of the following customer feedback text. 
Respond with ONLY a JSON object in this exact format:
{{
    "sentiment": "positive|neutral|negative",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}

Customer feedback: "{text}" """
        
        return await self._make_request(prompt, model)
    
    async def _make_request(self, prompt: str, model: str) -> Dict[str, Any]:
        # CRITICAL: Required headers for OpenRouter
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": settings.APP_URL or "https://localhost:3000",
            "X-Title": "AI Feedback Analyzer"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an expert at analyzing customer feedback. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 200,
            "temperature": 0.3,  # Low for consistency
            "stream": False  # MUST be False
        }
        
        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        
        response.raise_for_status()
        
        # Parse response and extract JSON
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # CRITICAL: Safely parse JSON response
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Extract JSON from response if wrapped in text
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise ValueError(f"Invalid JSON response: {content}")

# Task 4: Feedback Router
# backend/app/routers/feedback.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
import time

from app.database import get_async_session
from app.models.feedback import FeedbackEntry
from app.models.schemas import FeedbackCreate, FeedbackResponse, PaginatedResponse
from app.services.ai_service import OpenRouterClient
from app.utils.exceptions import AIServiceError

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

@router.post("/analyze", response_model=FeedbackResponse)
async def analyze_feedback(
    feedback: FeedbackCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Analyze new feedback with AI"""
    # Record start time
    start_time = time.time()
    
    # Initialize AI client
    ai_client = OpenRouterClient()
    
    try:
        # Get AI analysis
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
        
        return FeedbackResponse.model_validate(db_feedback)
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=PaginatedResponse[FeedbackResponse])
async def get_feedback_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sentiment: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session)
):
    """Get paginated feedback with filters"""
    # Build query
    query = select(FeedbackEntry)
    
    # Apply filters
    if sentiment:
        query = query.where(FeedbackEntry.sentiment == sentiment)
    if category:
        query = query.where(FeedbackEntry.category == category)
    if search:
        query = query.where(FeedbackEntry.text.ilike(f"%{search}%"))
    
    # Order by created_at desc
    query = query.order_by(FeedbackEntry.created_at.desc())
    
    # Get total count
    count_query = select(func.count()).select_from(FeedbackEntry)
    if sentiment:
        count_query = count_query.where(FeedbackEntry.sentiment == sentiment)
    if category:
        count_query = count_query.where(FeedbackEntry.category == category)
    if search:
        count_query = count_query.where(FeedbackEntry.text.ilike(f"%{search}%"))
    
    total = await db.scalar(count_query)
    
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
        pages=(total + page_size - 1) // page_size
    )
```

### Integration Points
```yaml
DATABASE:
  - migration: "alembic revision --autogenerate -m 'Initial feedback tables'"
  - migration: "alembic upgrade head"
  - index: "Already defined in model with index=True"
  
CONFIG:
  - add to: backend/app/config.py
  - pattern: |
      class Settings(BaseSettings):
          OPENROUTER_API_KEY: str
          DATABASE_URL: str = "sqlite+aiosqlite:///./feedback.db"
          CORS_ORIGINS: List[str] = ["http://localhost:5173"]
          APP_URL: Optional[str] = None
          LOG_LEVEL: str = "INFO"
          
          class Config:
              env_file = ".env"
  
ROUTES:
  - add to: backend/app/main.py
  - pattern: |
      from app.routers import feedback, analytics, health
      
      app.include_router(feedback.router)
      app.include_router(analytics.router)
      app.include_router(health.router)
      
MIDDLEWARE:
  - add to: backend/app/main.py
  - pattern: |
      from fastapi.middleware.cors import CORSMiddleware
      
      app.add_middleware(
          CORSMiddleware,
          allow_origins=settings.CORS_ORIGINS,
          allow_credentials=True,
          allow_methods=["*"],
          allow_headers=["*"],
      )
```

## Validation Loop

### Level 1: Syntax & Style (Backend)
```bash
# Navigate to backend directory
cd backend

# Install dependencies first
pip install -r requirements.txt

# Run these FIRST - fix any errors before proceeding
python -m py_compile app/**/*.py  # Syntax check
ruff check app/ --fix             # Auto-fix style issues
mypy app/                         # Type checking

# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests (Backend)
```python
# CREATE backend/app/tests/test_feedback.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_analyze_feedback():
    """Test feedback analysis endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/feedback/analyze",
            json={"text": "This product is amazing!", "tags": ["product"]}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] in ["positive", "neutral", "negative"]
    assert "category" in data

@pytest.mark.asyncio
async def test_get_feedback_list():
    """Test feedback list endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/feedback/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

@pytest.mark.asyncio
async def test_invalid_feedback():
    """Test validation errors"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/feedback/analyze",
            json={"text": "", "tags": []}
        )
    assert response.status_code == 422
```

```bash
# Run backend tests
cd backend
pytest app/tests/ -v

# If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Frontend Build & Lint
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run these checks
npm run type-check    # TypeScript validation
npm run lint         # ESLint checks
npm run build        # Build for production

# Expected: Successful build. Fix any errors.
```

### Level 4: Integration Test
```bash
# Terminal 1: Start backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev

# Terminal 3: Test the API
curl -X POST http://localhost:8000/api/feedback/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Great service but slow delivery", "tags": ["service", "delivery"]}'

# Expected: JSON response with sentiment and category
# If error: Check backend logs for stack trace

# Test health endpoint
curl http://localhost:8000/api/health

# Expected: {"status": "healthy", ...}
```

### Level 5: Full System Test
```bash
# Open browser to http://localhost:5173
# 1. Submit feedback through form
# 2. Check it appears in history
# 3. Test filters and search
# 4. View analytics page
# 5. Test tag editing
# 6. Test pagination

# Check browser console for errors
# Check network tab for failed requests
```

## Final Validation Checklist
- [ ] All backend tests pass: `cd backend && pytest app/tests/ -v`
- [ ] No linting errors: `cd backend && ruff check app/`
- [ ] No type errors: `cd backend && mypy app/`
- [ ] Frontend builds: `cd frontend && npm run build`
- [ ] No TypeScript errors: `cd frontend && npm run type-check`
- [ ] Manual test successful: Submit feedback and see analysis
- [ ] Error cases handled: Try empty text, long text, special characters
- [ ] Mobile responsive: Test on different screen sizes
- [ ] Analytics charts render: Check sentiment distribution
- [ ] Database migrations run: `cd backend && alembic upgrade head`

## Deployment Checklist
- [ ] Environment variables set in Vercel and Railway
- [ ] CORS configured for production URLs
- [ ] Database connection string updated for PostgreSQL
- [ ] API base URL updated in frontend
- [ ] Health checks passing in production
- [ ] Rate limiting active
- [ ] Error logging configured

## Common Issues & Solutions

### OpenRouter API Errors
- **401 Unauthorized**: Check API key and headers
- **429 Rate Limited**: Implement exponential backoff
- **Invalid JSON**: Add better parsing logic

### Database Issues
- **Connection errors**: Check DATABASE_URL format
- **Migration failures**: Drop tables and re-run
- **Async errors**: Use proper async context managers

### Frontend Issues
- **CORS errors**: Update backend CORS origins
- **API connection**: Check VITE_API_BASE_URL
- **Build size**: Lazy load large components

### Deployment Issues
- **Railway sleeping**: Add wake-up endpoint
- **Vercel 404**: Check vercel.json routing
- **Environment variables**: Double-check all services

## Success Metrics
- Feedback analysis completes in <2 seconds ✓
- Frontend bundle <500KB gzipped ✓
- All endpoints return proper status codes ✓
- Mobile responsive design works ✓
- Zero runtime errors in production ✓

## Confidence Score: 9/10

This PRP provides comprehensive context for one-pass implementation success. The only uncertainty is the specific OpenRouter API response format, which is handled with robust parsing logic and fallbacks.