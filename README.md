# AI Feedback Analyzer

A full-stack web application for AI-powered customer feedback analysis with sentiment classification, dynamic categorization, and comprehensive analytics dashboard.

## Features

- **AI-Powered Analysis**: Automatic sentiment analysis (positive/neutral/negative) and category classification
- **Real-time Processing**: Instant feedback analysis with <2 second response time
- **Analytics Dashboard**: Visual insights with charts and statistics
- **Tag Management**: Organize feedback with custom tags
- **Advanced Filtering**: Search and filter by sentiment, category, tags, and text
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Async ORM for database operations
- **OpenRouter API** - AI service for sentiment analysis
- **PostgreSQL/SQLite** - Database (SQLite for dev, PostgreSQL for production)
- **Alembic** - Database migrations

### Frontend
- **React 18** - UI library with TypeScript
- **Material-UI v5** - Component library
- **Redux Toolkit** - State management
- **Recharts** - Data visualization
- **Vite** - Build tool

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenRouter API key (get one at https://openrouter.ai)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

5. Add your OpenRouter API key to `.env`:
```
OPENROUTER_API_KEY=your_api_key_here
```

6. Initialize the database:
```bash
python -m app.utils.init_db
```

7. Run the backend server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5173

## API Documentation

Once the backend is running, you can access:
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## Testing

### Backend Tests
```bash
cd backend
pytest app/tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm run type-check
npm run lint
```

## Deployment

### Backend (Railway/Render)
1. Push your code to GitHub
2. Connect your repository to Railway/Render
3. Set environment variables
4. Deploy

### Frontend (Vercel)
1. Push your code to GitHub
2. Import project to Vercel
3. Set environment variables
4. Deploy

## Environment Variables

### Backend
- `OPENROUTER_API_KEY` - Your OpenRouter API key (required)
- `DATABASE_URL` - Database connection string
- `CORS_ORIGINS` - Allowed CORS origins
- `APP_URL` - Application URL for OpenRouter headers

### Frontend
- `VITE_API_BASE_URL` - Backend API URL

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── models/      # Database models
│   │   ├── routers/     # API endpoints
│   │   ├── services/    # Business logic
│   │   ├── utils/       # Utilities
│   │   └── main.py      # FastAPI app
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/  # React components
    │   ├── pages/       # Page components
    │   ├── store/       # Redux store
    │   ├── utils/       # Utilities
    │   └── App.tsx      # Main app component
    └── package.json
```

## License

MIT License
