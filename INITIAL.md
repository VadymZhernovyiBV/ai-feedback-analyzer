# AI Feedback Analyzer - Initial Project Specification

## FEATURE:
Build a production-ready web application for AI-powered customer feedback analysis with the following specific functionality:

### Core Features:
- **Feedback Analysis System**: Accept text feedback (up to 5000 characters) and analyze it using OpenRouter API to determine:
  - Sentiment classification (positive/neutral/negative) with confidence scores
  - Dynamic category classification with AI-generated categories
  - Processing time tracking and model attribution

- **Web Interface**: React 19 + TypeScript SPA with Material-UI v5 that includes:
  - Feedback submission form with real-time validation
  - Instant analysis results display
  - Feedback history with pagination (20 items per page)
  - Advanced filtering by sentiment, category, tags, and text search
  - Analytics dashboard showing sentiment distribution and top categories
  - Tag management system for organizing feedback entries

- **Backend API**: FastAPI-based REST API with:
  - POST `/api/feedback/analyze` - Analyze new feedback with AI
  - GET `/api/feedback` - Retrieve paginated history with filters
  - GET `/api/feedback/{id}` - Get specific feedback details
  - PUT `/api/feedback/{id}/tags` - Update feedback tags
  - DELETE `/api/feedback/{id}` - Delete feedback entry
  - GET `/api/stats` - Analytics and statistics
  - Health check endpoint with service status

- **Database**: SQLite for development, PostgreSQL for production with:
  - Feedback entries table with full analysis results
  - Proper indexing on created_at, sentiment, and category fields
  - JSON storage for tags array
  - Optional analysis logs table for debugging

### Technical Requirements:
- Anonymous usage (no authentication required)
- Responsive design for mobile and desktop
- Error handling with structured responses and fallbacks
- Rate limiting (100 req/min for analysis, 200 req/min for reads)
- Free hosting on Vercel (frontend) + Railway/Render (backend)

## DOCUMENTATION:

### API Documentation:
- **OpenRouter API**: https://openrouter.ai/docs
- **OpenRouter Models**: https://openrouter.ai/models
- **FastAPI**: https://fastapi.tiangolo.com/
- **FastAPI Best Practices**: https://fastapi.tiangolo.com/tutorial/best-practices/

### Frontend Libraries:
- **React 19 + TypeScript**: https://react.dev/learn/typescript
- **Material-UI v5**: https://mui.com/material-ui/getting-started/
- **Redux Toolkit**: https://redux-toolkit.js.org/introduction/getting-started
- **React Hook Form**: https://react-hook-form.com/get-started
- **Vite**: https://vitejs.dev/guide/

### Backend Libraries:
- **SQLAlchemy ORM**: https://docs.sqlalchemy.org/en/20/
- **Pydantic v2**: https://docs.pydantic.dev/latest/
- **httpx (async HTTP)**: https://www.python-httpx.org/
- **Alembic Migrations**: https://alembic.sqlalchemy.org/en/latest/

### Hosting Platforms:
- **Vercel Deployment**: https://vercel.com/docs/frameworks/vite
- **Railway Python Guide**: https://docs.railway.app/guides/python
- **Render FastAPI**: https://render.com/docs/deploy-fastapi

### Database:
- **PostgreSQL JSON**: https://www.postgresql.org/docs/current/datatype-json.html
- **SQLite to PostgreSQL Migration**: https://docs.sqlalchemy.org/en/20/core/engines.html

## OTHER CONSIDERATIONS:

### Critical Implementation Details AI Assistants Often Miss:

1. **OpenRouter API Integration**:
   - Must include `HTTP-Referer` and `X-Title` headers for free tier access
   - Implement fallback to free models (meta-llama/llama-3.1-8b-instruct:free) when primary model fails
   - Parse AI responses as JSON - responses must be validated before storage
   - Temperature should be set to 0.3 for consistent classification results

2. **Database Design Gotchas**:
   - Tags must be stored as JSON TEXT in SQLite but can use JSONB in PostgreSQL
   - Always use UTC timestamps (TIMESTAMP, not TIMESTAMPTZ)
   - Sentiment values must be constrained to enum: 'positive', 'neutral', 'negative'
   - Include analysis_duration_ms and model_used fields for debugging

3. **Frontend State Management**:
   - Use Redux Toolkit with normalized state structure, not Context API
   - Implement proper loading states for all async operations
   - Form submission should show instant feedback while analysis processes
   - Virtual scrolling required for feedback lists over 100 items

4. **Error Handling Requirements**:
   - All errors must follow consistent format: `{error: "code", message: "text", details: {}}`
   - Implement exponential backoff for rate-limited requests
   - Never expose internal error details to frontend
   - Log all AI service failures with full request/response for debugging

5. **Performance Constraints**:
   - Frontend bundle size must be under 500KB (gzipped)
   - API response time target: <2s for analysis, <200ms for reads
   - Implement response caching for identical feedback texts
   - Use database connection pooling in production

6. **Deployment Specifics**:
   - Environment variables must be properly configured in both Vercel and Railway
   - CORS must be configured to allow only the Vercel frontend URL
   - Database migrations must run automatically on deployment
   - Health checks must verify both database and AI service connectivity

7. **Free Tier Limitations**:
   - Railway free tier sleeps after inactivity - implement wake-up strategy
   - OpenRouter free tier has rate limits - implement queuing
   - Monitor usage to stay within free tier limits
   - Implement data retention policy (e.g., delete entries older than 30 days)

8. **Common Mistakes to Avoid**:
   - Don't use OpenAI SDK directly - use httpx for OpenRouter compatibility
   - Don't store sensitive data in feedback text
   - Don't implement authentication initially - keep it simple
   - Don't use Server-Side Rendering - static SPA is sufficient
   - Don't forget to set `stream: false` in OpenRouter requests
