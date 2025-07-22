# AI Feedback Analyzer - INITIAL.md

## FEATURE

The AI Feedback Analyzer is a web-based platform that automatically analyzes customer feedback using AI/ML to determine emotional tone and categorize feedback. The system consists of:

**Core Functionality:**
- Text feedback submission (up to 5000 characters, English-only)
- AI-powered sentiment analysis (positive/neutral/negative with confidence scores)
- Dynamic category classification via LLM (e.g., "Product Quality", "Customer Service", "Delivery")
- Feedback history management with filtering, sorting, and search
- Tag management system for organizing feedback
- Analytics dashboard with sentiment distribution and category insights
- Anonymous usage (no authentication required)

**Technical Architecture:**
- **Frontend**: React 19 (vite) + TypeScript, Vite, React Router v6, Redux Toolkit, Material-UI v5
- **Backend**: Python 3.12+ with FastAPI, SQLAlchemy ORM
- **AI Service**: OpenRouter API integration (free tier) with fallback to rule-based analysis
- **Database**: SQLite (development) / PostgreSQL (production)
- **Hosting**: Vercel (frontend) + Railway/Render (backend) - all free tiers

**Key Features:**
- Real-time feedback analysis with confidence scoring
- Responsive Material-UI interface with light/dark theme support
- Advanced filtering and pagination for feedback history
- Analytics with charts showing sentiment trends and category distribution
- Tag-based organization system
- Error handling with graceful fallbacks
- Rate limiting and cost management for AI API usage

## DOCUMENTATION

Key documentation sources that will be referenced during development:

**Framework Documentation:**
- FastAPI Official Docs: https://fastapi.tiangolo.com/
- React 18 Documentation: https://react.dev/
- Material-UI v5 Docs: https://mui.com/material-ui/
- Redux Toolkit Documentation: https://redux-toolkit.js.org/
- React Router v6 Guide: https://reactrouter.com/en/main
- SQLAlchemy 2.0 Documentation: https://docs.sqlalchemy.org/en/20/

**AI Integration:**
- OpenRouter API Documentation: https://openrouter.ai/docs
- OpenAI API Reference (for prompt engineering): https://platform.openai.com/docs/api-reference
- LLM Prompt Engineering Guide: https://www.promptingguide.ai/

**Deployment & Hosting:**
- Vercel Documentation: https://vercel.com/docs
- Railway Documentation: https://docs.railway.app/
- Render Documentation: https://render.com/docs
- Docker Best Practices: https://docs.docker.com/develop/dev-best-practices/

**Database & ORM:**
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- SQLite Documentation: https://www.sqlite.org/docs.html
- Alembic Migration Guide: https://alembic.sqlalchemy.org/en/latest/

**Testing & Quality:**
- Pytest Documentation: https://docs.pytest.org/
- React Testing Library: https://testing-library.com/docs/react-testing-library/intro/
- TypeScript Handbook: https://www.typescriptlang.org/docs/

## OTHER CONSIDERATIONS

**Critical Implementation Gotchas:**

1. **CORS Configuration**: Backend must properly configure CORS for Vercel frontend domain. Use environment variable for allowed origins, not hardcoded values.

2. **OpenRouter API Rate Limits**: Free tier has strict limits. Implement proper queuing, exponential backoff, and fallback to rule-based analysis when API fails.

3. **Environment Variables**: 
   - Backend needs `OPENROUTER_API_KEY`, `DATABASE_URL`, `CORS_ORIGINS`
   - Frontend needs `VITE_API_BASE_URL` (note the VITE_ prefix for Vite)
   - Never commit API keys to version control

4. **Database Schema Sync**: Use Alembic migrations for schema changes. SQLite for development, PostgreSQL for production - ensure compatibility.

5. **AI Response Parsing**: OpenRouter responses may not always be valid JSON. Implement robust parsing with try/catch and fallback responses.

6. **Free Hosting Limitations**:
   - Railway/Render free tier sleeps after inactivity - implement health check endpoints
   - Vercel has 100GB bandwidth limit - optimize bundle size
   - PostgreSQL free tier has 1GB storage limit - implement data cleanup

7. **Material-UI Theme**: Use consistent theme provider and avoid inline styles. Implement proper responsive breakpoints.

8. **Redux State Management**: Use RTK Query for API calls, avoid manual fetch in components. Implement proper error states and loading indicators.

9. **Form Validation**: Use React Hook Form with Yup schemas. Validate on both frontend and backend. Handle 5000 character limit for feedback text.

10. **Error Boundaries**: Implement React error boundaries to catch component crashes. Log errors for debugging.

**Performance Considerations:**
- Implement virtual scrolling for large feedback lists
- Use React.memo for expensive components
- Debounce search inputs to avoid excessive API calls
- Cache AI analysis results to avoid duplicate processing
- Optimize bundle size with code splitting

**Security Considerations:**
- Sanitize all user inputs on backend
- Implement rate limiting on all endpoints
- Use HTTPS in production (automatic with Vercel/Railway)
- No authentication required, but implement basic input validation

**Common AI Assistant Pitfalls to Avoid:**
- Don't hardcode API endpoints - use environment variables
- Don't forget to handle AI API failures gracefully
- Don't use deprecated Material-UI v4 syntax (use v5)
- Don't forget to implement proper TypeScript interfaces
- Don't skip error handling for async operations
- Don't use class components - use functional components with hooks
- Don't forget to implement loading states for all async operations
- Don't hardcode database connection strings
- Don't forget CORS configuration for cross-origin requests
- Don't skip input validation on both frontend and backend