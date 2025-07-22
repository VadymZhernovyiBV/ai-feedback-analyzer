# AI Feedback Analyzer - Technical Specification

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Database Schema](#database-schema)
4. [API Design](#api-design)
5. [Frontend Architecture](#frontend-architecture)
6. [AI Integration Strategy](#ai-integration-strategy)
7. [Free Hosting Solutions](#free-hosting-solutions)
8. [Project Structure](#project-structure)
9. [Environment Setup](#environment-setup)
10. [Implementation Roadmap](#implementation-roadmap)
11. [Technical Decisions Rationale](#technical-decisions-rationale)

## Project Overview

### Purpose
A web-based platform for analyzing customer feedback using AI/ML to determine emotional tone (sentiment) and categorize feedback automatically. Users can submit text feedback, view analysis results, and manage their feedback history.

### Key Features
- Text feedback submission and analysis
- AI-powered sentiment analysis (positive/neutral/negative)
- Dynamic category classification via LLM
- Feedback history with filtering and sorting
- Tag management system
- Anonymous usage (no authentication required)
- Responsive web interface

### Technology Stack
- **Frontend**: React 19 + TypeScript, Vite, React Router v6, Redux Toolkit, Material-UI v5
- **Backend**: Python 3.12+ with FastAPI
- **AI Service**: OpenRouter API (free tier)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Hosting**: Vercel (frontend) + Railway/Render (backend)

## System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React SPA     │    │   FastAPI       │    │   OpenRouter    │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   API Service   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   SQLite/       │
                       │   PostgreSQL    │
                       │   (Database)    │
                       └─────────────────┘
```

### Data Flow
1. User submits feedback text via React frontend
2. Frontend sends POST request to FastAPI backend
3. Backend validates input and calls OpenRouter API for analysis
4. OpenRouter returns sentiment and category analysis
5. Backend stores results in database
6. Backend returns analysis to frontend
7. Frontend displays results and updates history

### Component Interaction
- **Frontend**: Handles UI/UX, form validation, state management, API calls
- **Backend**: Business logic, data validation, AI service integration, database operations
- **AI Service**: Sentiment analysis and category classification
- **Database**: Persistent storage for feedback entries and analysis results

## Database Schema

### Tables

#### `feedback_entries`
```sql
CREATE TABLE feedback_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    sentiment_confidence REAL,
    category VARCHAR(100),
    category_confidence REAL,
    tags TEXT, -- JSON array of strings
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analysis_duration_ms INTEGER,
    model_used VARCHAR(50)
);
```

#### `analysis_logs` (Optional - for debugging)
```sql
CREATE TABLE analysis_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feedback_id INTEGER,
    request_payload TEXT,
    response_payload TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (feedback_id) REFERENCES feedback_entries(id)
);
```

### Indexes
```sql
CREATE INDEX idx_feedback_created_at ON feedback_entries(created_at);
CREATE INDEX idx_feedback_sentiment ON feedback_entries(sentiment);
CREATE INDEX idx_feedback_category ON feedback_entries(category);
```

### Data Types & Constraints
- **Text**: Max 5000 characters for feedback text
- **Sentiment**: Enum values: 'positive', 'neutral', 'negative'
- **Confidence**: Float between 0.0 and 1.0
- **Tags**: JSON array stored as TEXT
- **Timestamps**: ISO 8601 format

## API Design

### Base URL
- Development: `http://localhost:8000`
- Production: `https://your-app-backend.railway.app`

### Authentication
No authentication required (anonymous usage)

### Endpoints

#### POST `/api/feedback/analyze`
Analyze new feedback text.

**Request:**
```json
{
    "text": "The product is amazing but delivery was slow",
    "tags": ["product", "delivery"] // optional
}
```

**Response (200):**
```json
{
    "id": 123,
    "text": "The product is amazing but delivery was slow",
    "sentiment": "neutral",
    "sentiment_confidence": 0.75,
    "category": "Product & Delivery",
    "category_confidence": 0.89,
    "tags": ["product", "delivery"],
    "created_at": "2025-07-22T10:30:00Z",
    "analysis_duration_ms": 1250,
    "model_used": "openai/gpt-3.5-turbo"
}
```

**Error Responses:**
```json
// 400 - Validation Error
{
    "error": "validation_error",
    "message": "Text is required and must be between 1 and 5000 characters",
    "details": {
        "field": "text",
        "constraint": "length"
    }
}

// 429 - Rate Limit
{
    "error": "rate_limit_exceeded",
    "message": "Too many requests. Please try again later.",
    "retry_after": 60
}

// 503 - AI Service Unavailable
{
    "error": "ai_service_unavailable",
    "message": "AI analysis service is temporarily unavailable",
    "fallback_available": false
}
```

#### GET `/api/feedback`
Retrieve feedback history with filtering and pagination.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)
- `sentiment`: Filter by sentiment ('positive', 'neutral', 'negative')
- `category`: Filter by category (exact match)
- `tag`: Filter by tag (exact match)
- `sort`: Sort field ('created_at', 'sentiment', 'category')
- `order`: Sort order ('asc', 'desc', default: 'desc')
- `search`: Text search in feedback content

**Response (200):**
```json
{
    "data": [
        {
            "id": 123,
            "text": "The product is amazing...",
            "sentiment": "positive",
            "sentiment_confidence": 0.92,
            "category": "Product Quality",
            "category_confidence": 0.88,
            "tags": ["product"],
            "created_at": "2025-07-22T10:30:00Z"
        }
    ],
    "pagination": {
        "page": 1,
        "limit": 20,
        "total": 45,
        "pages": 3,
        "has_next": true,
        "has_prev": false
    },
    "filters": {
        "sentiment": null,
        "category": null,
        "tag": null,
        "search": null
    }
}
```

#### GET `/api/feedback/{id}`
Get specific feedback entry by ID.

**Response (200):**
```json
{
    "id": 123,
    "text": "The product is amazing but delivery was slow",
    "sentiment": "neutral",
    "sentiment_confidence": 0.75,
    "category": "Product & Delivery",
    "category_confidence": 0.89,
    "tags": ["product", "delivery"],
    "created_at": "2025-07-22T10:30:00Z",
    "updated_at": "2025-07-22T10:30:00Z",
    "analysis_duration_ms": 1250,
    "model_used": "openai/gpt-3.5-turbo"
}
```

#### PUT `/api/feedback/{id}/tags`
Update tags for a feedback entry.

**Request:**
```json
{
    "tags": ["product", "delivery", "customer-service"]
}
```

**Response (200):**
```json
{
    "id": 123,
    "tags": ["product", "delivery", "customer-service"],
    "updated_at": "2025-07-22T11:15:00Z"
}
```

#### DELETE `/api/feedback/{id}`
Delete a feedback entry.

**Response (204):** No content

#### GET `/api/stats`
Get analytics and statistics.

**Response (200):**
```json
{
    "total_entries": 156,
    "sentiment_distribution": {
        "positive": 89,
        "neutral": 45,
        "negative": 22
    },
    "top_categories": [
        {"category": "Product Quality", "count": 34},
        {"category": "Customer Service", "count": 28},
        {"category": "Delivery", "count": 19}
    ],
    "recent_activity": {
        "last_7_days": 23,
        "last_30_days": 67
    }
}
```

#### GET `/api/health`
Health check endpoint.

**Response (200):**
```json
{
    "status": "healthy",
    "timestamp": "2025-07-22T10:30:00Z",
    "version": "1.0.0",
    "services": {
        "database": "connected",
        "ai_service": "available"
    }
}
```

### Error Handling Standards
- Use appropriate HTTP status codes
- Consistent error response format
- Include error codes for programmatic handling
- Provide helpful error messages
- Log errors server-side for debugging

### Rate Limiting
- 100 requests per minute per IP for analysis endpoint
- 200 requests per minute per IP for read endpoints
- Implement exponential backoff suggestions

## Frontend Architecture

### Component Hierarchy
```
App
├── Router
│   ├── Layout
│   │   ├── Header
│   │   ├── Navigation
│   │   └── Footer
│   ├── Pages
│   │   ├── HomePage
│   │   │   ├── FeedbackForm
│   │   │   └── RecentAnalysis
│   │   ├── HistoryPage
│   │   │   ├── FilterPanel
│   │   │   ├── FeedbackList
│   │   │   │   └── FeedbackCard
│   │   │   └── Pagination
│   │   ├── AnalyticsPage
│   │   │   ├── StatsCards
│   │   │   ├── SentimentChart
│   │   │   └── CategoryChart
│   │   └── FeedbackDetailPage
│   │       ├── FeedbackDetails
│   │       └── TagEditor
│   └── Components (Shared)
│       ├── LoadingSpinner
│       ├── ErrorBoundary
│       ├── ConfirmDialog
│       └── Toast
```

### State Management (Redux Toolkit)

#### Store Structure
```typescript
interface RootState {
    feedback: FeedbackState;
    ui: UIState;
    analytics: AnalyticsState;
}

interface FeedbackState {
    entries: FeedbackEntry[];
    currentEntry: FeedbackEntry | null;
    loading: boolean;
    error: string | null;
    pagination: PaginationInfo;
    filters: FilterState;
}

interface UIState {
    theme: 'light' | 'dark';
    sidebarOpen: boolean;
    notifications: Notification[];
}

interface AnalyticsState {
    stats: StatsData | null;
    loading: boolean;
    error: string | null;
}
```

#### Slices
- `feedbackSlice`: Manage feedback entries, analysis, CRUD operations
- `uiSlice`: UI state, theme, notifications
- `analyticsSlice`: Statistics and analytics data

### Routing Structure
```typescript
const routes = [
    {
        path: '/',
        element: <Layout />,
        children: [
            { index: true, element: <HomePage /> },
            { path: 'history', element: <HistoryPage /> },
            { path: 'analytics', element: <AnalyticsPage /> },
            { path: 'feedback/:id', element: <FeedbackDetailPage /> },
            { path: '*', element: <NotFoundPage /> }
        ]
    }
];
```

### Key Components

#### FeedbackForm
```typescript
interface FeedbackFormProps {
    onSubmit: (data: FeedbackSubmission) => void;
    loading?: boolean;
}

interface FeedbackSubmission {
    text: string;
    tags?: string[];
}
```

#### FeedbackCard
```typescript
interface FeedbackCardProps {
    feedback: FeedbackEntry;
    onTagUpdate?: (id: number, tags: string[]) => void;
    onDelete?: (id: number) => void;
    compact?: boolean;
}
```

#### FilterPanel
```typescript
interface FilterPanelProps {
    filters: FilterState;
    onFilterChange: (filters: Partial<FilterState>) => void;
    availableCategories: string[];
    availableTags: string[];
}
```

### Material-UI Theme
```typescript
const theme = createTheme({
    palette: {
        primary: {
            main: '#1976d2',
        },
        secondary: {
            main: '#dc004e',
        },
        background: {
            default: '#f5f5f5',
        },
    },
    typography: {
        h4: {
            fontWeight: 600,
        },
    },
    components: {
        MuiCard: {
            styleOverrides: {
                root: {
                    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                },
            },
        },
    },
});
```

### Form Validation
- Use React Hook Form with Yup schema validation
- Real-time validation feedback
- Accessible error messages

### Performance Optimizations
- React.memo for expensive components
- useMemo for computed values
- useCallback for event handlers
- Lazy loading for routes
- Virtual scrolling for large lists

## AI Integration Strategy

### OpenRouter API Integration

#### Configuration
```python
OPENROUTER_API_KEY = "your-api-key"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-3.5-turbo"
FALLBACK_MODEL = "meta-llama/llama-3.1-8b-instruct:free"
```

#### Prompt Engineering

**Sentiment Analysis Prompt:**
```python
SENTIMENT_PROMPT = """
Analyze the sentiment of the following customer feedback text. 
Respond with ONLY a JSON object in this exact format:
{
    "sentiment": "positive|neutral|negative",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}

Customer feedback: "{feedback_text}"
"""
```

**Category Classification Prompt:**
```python
CATEGORY_PROMPT = """
Categorize the following customer feedback into the most appropriate category.
Choose or create a concise, descriptive category name (2-4 words max).
Common categories include: Product Quality, Customer Service, Delivery, Pricing, User Experience, Technical Issues, etc.

Respond with ONLY a JSON object in this exact format:
{
    "category": "Category Name",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}

Customer feedback: "{feedback_text}"
"""
```

#### API Client Implementation
```python
import httpx
import json
from typing import Dict, Any, Optional

class OpenRouterClient:
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def analyze_sentiment(self, text: str, model: str = "openai/gpt-3.5-turbo") -> Dict[str, Any]:
        prompt = SENTIMENT_PROMPT.format(feedback_text=text)
        return await self._make_request(prompt, model)
    
    async def categorize_feedback(self, text: str, model: str = "openai/gpt-3.5-turbo") -> Dict[str, Any]:
        prompt = CATEGORY_PROMPT.format(feedback_text=text)
        return await self._make_request(prompt, model)
    
    async def _make_request(self, prompt: str, model: str) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-app.example.com",
            "X-Title": "AI Feedback Analyzer"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an expert at analyzing customer feedback."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 200,
            "temperature": 0.3,
            "stream": False
        }
        
        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return json.loads(content)
        else:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
```

#### Error Handling & Fallbacks
```python
async def analyze_feedback_with_fallback(text: str) -> Dict[str, Any]:
    models = ["openai/gpt-3.5-turbo", "meta-llama/llama-3.1-8b-instruct:free"]
    
    for model in models:
        try:
            sentiment_result = await client.analyze_sentiment(text, model)
            category_result = await client.categorize_feedback(text, model)
            
            return {
                "sentiment": sentiment_result["sentiment"],
                "sentiment_confidence": sentiment_result["confidence"],
                "category": category_result["category"],
                "category_confidence": category_result["confidence"],
                "model_used": model
            }
        except Exception as e:
            logger.warning(f"Model {model} failed: {e}")
            continue
    
    # Ultimate fallback - rule-based analysis
    return rule_based_analysis(text)

def rule_based_analysis(text: str) -> Dict[str, Any]:
    """Simple rule-based fallback when AI services are unavailable"""
    positive_words = ["good", "great", "excellent", "amazing", "love", "perfect"]
    negative_words = ["bad", "terrible", "awful", "hate", "worst", "horrible"]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        sentiment = "positive"
    elif negative_count > positive_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {
        "sentiment": sentiment,
        "sentiment_confidence": 0.6,
        "category": "General Feedback",
        "category_confidence": 0.5,
        "model_used": "rule_based_fallback"
    }
```

#### Rate Limiting & Caching
- Implement request queuing for rate limit compliance
- Cache analysis results to avoid duplicate API calls
- Use Redis for production caching (optional)

#### Cost Management
- Monitor API usage and costs
- Implement daily/monthly usage limits
- Use free tier models when possible
- Batch requests when feasible

## Free Hosting Solutions

### Frontend Hosting: Vercel

**Why Vercel:**
- Excellent React/Vite support
- Automatic deployments from Git
- Global CDN
- Free tier: 100GB bandwidth, unlimited personal projects
- Built-in analytics and performance monitoring

**Deployment Configuration:**
```json
// vercel.json
{
    "builds": [
        {
            "src": "package.json",
            "use": "@vercel/static-build",
            "config": {
                "distDir": "dist"
            }
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "/index.html"
        }
    ],
    "env": {
        "VITE_API_BASE_URL": "https://your-backend.railway.app"
    }
}
```

### Backend Hosting: Railway

**Why Railway:**
- Simple Python/FastAPI deployment
- PostgreSQL database included
- Free tier: $5/month credit, 512MB RAM, 1GB disk
- Automatic HTTPS
- Environment variable management

**Alternative: Render**
- Free tier: 512MB RAM, sleeps after 15min inactivity
- PostgreSQL free tier: 1GB storage
- Automatic deployments from Git

**Deployment Configuration:**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# railway.toml
[build]
builder = "DOCKERFILE"

[deploy]
healthcheckPath = "/api/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### Database Options

**Development: SQLite**
- File-based, no setup required
- Perfect for local development
- Easy to backup and migrate

**Production: PostgreSQL (Railway/Render)**
- Railway: Free 1GB PostgreSQL
- Render: Free 1GB PostgreSQL
- Automatic backups
- Connection pooling

### Environment Variables
```bash
# Backend (.env)
OPENROUTER_API_KEY=your_openrouter_api_key
DATABASE_URL=postgresql://user:pass@host:port/db
CORS_ORIGINS=https://your-frontend.vercel.app
LOG_LEVEL=INFO

# Frontend (.env)
VITE_API_BASE_URL=https://your-backend.railway.app
VITE_APP_NAME=AI Feedback Analyzer
```

## Project Structure

### Backend Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database connection and models
│   ├── models/
│   │   ├── __init__.py
│   │   ├── feedback.py        # SQLAlchemy models
│   │   └── schemas.py         # Pydantic schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── feedback.py        # Feedback endpoints
│   │   ├── analytics.py       # Analytics endpoints
│   │   └── health.py          # Health check
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py      # OpenRouter integration
│   │   ├── feedback_service.py # Business logic
│   │   └── analytics_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py      # Input validation
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── logging.py         # Logging configuration
│   └── tests/
│       ├── __init__.py
│       ├── test_feedback.py
│       ├── test_ai_service.py
│       └── conftest.py
├── requirements.txt
├── Dockerfile
├── railway.toml
├── .env.example
└── README.md
```

### Frontend Structure
```
frontend/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── main.tsx               # App entry point
│   ├── App.tsx                # Root component
│   ├── components/
│   │   ├── common/
│   │   │   ├── LoadingSpinner.tsx
│   │   │   ├── ErrorBoundary.tsx
│   │   │   ├── ConfirmDialog.tsx
│   │   │   └── Toast.tsx
│   │   ├── feedback/
│   │   │   ├── FeedbackForm.tsx
│   │   │   ├── FeedbackCard.tsx
│   │   │   ├── FeedbackList.tsx
│   │   │   └── TagEditor.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Navigation.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Layout.tsx
│   │   └── analytics/
│   │       ├── StatsCards.tsx
│   │       ├── SentimentChart.tsx
│   │       └── CategoryChart.tsx
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── HistoryPage.tsx
│   │   ├── AnalyticsPage.tsx
│   │   ├── FeedbackDetailPage.tsx
│   │   └── NotFoundPage.tsx
│   ├── store/
│   │   ├── index.ts           # Store configuration
│   │   ├── slices/
│   │   │   ├── feedbackSlice.ts
│   │   │   ├── uiSlice.ts
│   │   │   └── analyticsSlice.ts
│   │   └── api/
│   │       └── feedbackApi.ts # RTK Query API
│   ├── hooks/
│   │   ├── useDebounce.ts
│   │   ├── usePagination.ts
│   │   └── useLocalStorage.ts
│   ├── utils/
│   │   ├── api.ts             # API client
│   │   ├── constants.ts       # App constants
│   │   ├── formatters.ts      # Data formatters
│   │   └── validators.ts      # Form validation
│   ├── types/
│   │   ├── feedback.ts        # TypeScript interfaces
│   │   ├── api.ts
│   │   └── common.ts
│   ├── styles/
│   │   ├── theme.ts           # Material-UI theme
│   │   └── globals.css
│   └── tests/
│       ├── components/
│       ├── pages/
│       ├── utils/
│       └── setup.ts
├── package.json
├── tsconfig.json
├── vite.config.ts
├── vercel.json
├── .env.example
└── README.md
```

## Environment Setup

### Development Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.11+
- Git
- Code editor (VS Code recommended)

### Backend Setup
```bash
# Clone repository
git clone <repository-url>
cd ai-feedback-analyzer/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenRouter API key

# Initialize database
python -c "from app.database import create_tables; create_tables()"

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with backend URL

# Run development server
npm run dev
```

### Required Dependencies

**Backend (requirements.txt):**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pydantic==2.5.0
httpx==0.25.2
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1
```

**Frontend (package.json):**
```json
{
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "react-router-dom": "^6.20.0",
        "@reduxjs/toolkit": "^1.9.7",
        "react-redux": "^8.1.3",
        "@mui/material": "^5.14.18",
        "@mui/icons-material": "^5.14.18",
        "@emotion/react": "^11.11.1",
        "@emotion/styled": "^11.11.0",
        "react-hook-form": "^7.48.2",
        "yup": "^1.3.3",
        "@hookform/resolvers": "^3.3.2",
        "recharts": "^2.8.0",
        "date-fns": "^2.30.0"
    },
    "devDependencies": {
        "@types/react": "^18.2.37",
        "@types/react-dom": "^18.2.15",
        "@typescript-eslint/eslint-plugin": "^6.10.0",
        "@typescript-eslint/parser": "^6.10.0",
        "@vitejs/plugin-react": "^4.1.1",
        "eslint": "^8.53.0",
        "eslint-plugin-react-hooks": "^4.6.0",
        "eslint-plugin-react-refresh": "^0.4.4",
        "typescript": "^5.2.2",
        "vite": "^4.5.0",
        "@testing-library/react": "^13.4.0",
        "@testing-library/jest-dom": "^5.16.5",
        "vitest": "^0.34.6"
    }
}
```

### Development Tools
- **VS Code Extensions**: Python, TypeScript, ES7+ React/Redux/React-Native snippets
- **Database Tools**: DB Browser for SQLite, pgAdmin for PostgreSQL
- **API Testing**: Postman, Thunder Client
- **Version Control**: Git with conventional commits

## Implementation Roadmap

### Phase 1: Core Backend (Week 1)
**Priority: High**
- [ ] Set up FastAPI project structure
- [ ] Implement database models and migrations
- [ ] Create basic CRUD endpoints for feedback
- [ ] Set up OpenRouter API integration
- [ ] Implement sentiment analysis endpoint
- [ ] Add basic error handling and logging
- [ ] Write unit tests for core functionality

**Deliverables:**
- Working API with feedback analysis
- Database schema implemented
- Basic documentation

### Phase 2: Core Frontend (Week 2)
**Priority: High**
- [ ] Set up React + TypeScript + Vite project
- [ ] Implement basic routing structure
- [ ] Create feedback submission form
- [ ] Build feedback display components
- [ ] Set up Redux store and slices
- [ ] Implement API integration
- [ ] Add basic styling with Material-UI

**Deliverables:**
- Functional web interface
- Feedback submission and display
- Responsive design

### Phase 3: Enhanced Features (Week 3)
**Priority: Medium**
- [ ] Add category classification
- [ ] Implement feedback history with pagination
- [ ] Create filtering and sorting functionality
- [ ] Add tag management system
- [ ] Build analytics dashboard
- [ ] Implement search functionality
- [ ] Add data export capabilities

**Deliverables:**
- Complete feature set
- Analytics dashboard
- Advanced filtering

### Phase 4: Polish & Deployment (Week 4)
**Priority: Medium**
- [ ] Comprehensive error handling
- [ ] Performance optimizations
- [ ] Accessibility improvements
- [ ] Mobile responsiveness
- [ ] Deploy to production hosting
- [ ] Set up monitoring and logging
- [ ] Write user documentation

**Deliverables:**
- Production-ready application
- Deployed and accessible
- Complete documentation

### Phase 5: Advanced Features (Future)
**Priority: Low**
- [ ] Real-time updates with WebSockets
- [ ] Bulk feedback import/export
- [ ] Advanced analytics and reporting
- [ ] Custom category training
- [ ] API rate limiting dashboard
- [ ] Multi-language support
- [ ] User authentication (optional)

### Testing Strategy
- **Unit Tests**: Core business logic, API endpoints
- **Integration Tests**: Database operations, AI service integration
- **E2E Tests**: Critical user flows
- **Performance Tests**: API response times, database queries
- **Security Tests**: Input validation, SQL injection prevention

### Quality Assurance
- Code reviews for all major features
- Automated testing in CI/CD pipeline
- Performance monitoring and optimization
- Security vulnerability scanning
- Accessibility testing with screen readers

## Technical Decisions Rationale

### Technology Stack Choices

#### Frontend: React + TypeScript + Vite
**Rationale:**
- **React**: Mature ecosystem, excellent community support, component reusability
- **TypeScript**: Type safety reduces bugs, better IDE support, improved maintainability
- **Vite**: Fast development server, optimized builds, excellent TypeScript support
- **Material-UI**: Comprehensive component library, accessibility built-in, consistent design

**Alternatives Considered:**
- Vue.js: Less ecosystem maturity for this use case
- Angular: Overkill for project scope
- Plain JavaScript: Lack of type safety for larger codebase

#### Backend: FastAPI + Python
**Rationale:**
- **FastAPI**: Automatic API documentation, excellent async support, type hints integration
- **Python**: Rich AI/ML ecosystem, readable code, extensive libraries
- **SQLAlchemy**: Mature ORM, database agnostic, migration support
- **Pydantic**: Data validation, serialization, integrates well with FastAPI

**Alternatives Considered:**
- Node.js/Express: Less suitable for AI integration
- Django: Too heavyweight for API-only backend
- Flask: Less modern features compared to FastAPI

#### Database: SQLite → PostgreSQL
**Rationale:**
- **SQLite**: Perfect for development, no setup required, easy testing
- **PostgreSQL**: Production-ready, excellent JSON support, free hosting available
- **Migration Path**: SQLAlchemy makes database switching seamless

**Alternatives Considered:**
- MongoDB: Overkill for structured data
- MySQL: PostgreSQL has better JSON support
- In-memory: Not suitable for persistent storage

#### AI Service: OpenRouter
**Rationale:**
- **Cost-Effective**: Free tier available, competitive pricing
- **Model Variety**: Access to multiple AI models, fallback options
- **OpenAI Compatible**: Standard API format, easy integration
- **Reliability**: Established service with good uptime

**Alternatives Considered:**
- Direct OpenAI API: More expensive, single provider
- Hugging Face: More complex setup, hosting requirements
- Local models: Resource intensive, deployment complexity

#### Hosting: Vercel + Railway
**Rationale:**
- **Vercel**: Excellent React support, global CDN, generous free tier
- **Railway**: Simple deployment, database included, reasonable free tier
- **Separation**: Frontend/backend separation allows independent scaling

**Alternatives Considered:**
- Netlify + Heroku: Heroku no longer has free tier
- AWS/GCP: Too complex for simple project
- Single platform: Less flexibility for optimization

### Architecture Decisions

#### Monorepo vs Separate Repositories
**Decision**: Separate repositories
**Rationale**: Independent deployment cycles, different technology stacks, clearer separation of concerns

#### State Management: Redux Toolkit
**Decision**: Redux Toolkit over Context API
**Rationale**: Better DevTools, middleware support, normalized state management, scalability

#### API Design: RESTful
**Decision**: REST over GraphQL
**Rationale**: Simpler implementation, better caching, sufficient for project needs, easier debugging

#### Authentication: Anonymous
**Decision**: No authentication initially
**Rationale**: Reduces complexity, faster development, suitable for demo/learning project

#### Error Handling Strategy
**Decision**: Structured error responses with codes
**Rationale**: Enables programmatic error handling, better user experience, easier debugging

### Performance Considerations

#### Frontend Optimizations
- Code splitting with React.lazy()
- Memoization for expensive computations
- Virtual scrolling for large lists
- Image optimization and lazy loading
- Bundle size monitoring

#### Backend Optimizations
- Database indexing on frequently queried fields
- Connection pooling for database
- Async/await for I/O operations
- Response caching for analytics endpoints
- Request rate limiting

#### AI Service Optimizations
- Response caching to avoid duplicate API calls
- Request batching where possible
- Fallback to simpler models on failure
- Usage monitoring and cost control

### Security Considerations

#### Input Validation
- Server-side validation for all inputs
- SQL injection prevention with parameterized queries
- XSS prevention with proper escaping
- File upload restrictions (if implemented)

#### API Security
- CORS configuration for production
- Rate limiting to prevent abuse
- Request size limits
- Error message sanitization

#### Data Privacy
- No personal data collection
- Feedback text stored securely
- Optional data retention policies
- GDPR compliance considerations

### Scalability Considerations

#### Database Scaling
- Proper indexing strategy
- Query optimization
- Connection pooling
- Read replicas (future consideration)

#### Application Scaling
- Stateless backend design
- Horizontal scaling capability
- Caching strategies
- CDN utilization

#### Cost Management
- AI API usage monitoring
- Free tier optimization
- Resource usage tracking
- Automated cost alerts

This comprehensive specification provides a complete roadmap for implementing the AI Feedback Analyzer project. Each section includes detailed technical requirements, implementation guidelines, and rationale for design decisions. The specification is designed to be actionable and comprehensive enough for any developer to successfully implement the project.
