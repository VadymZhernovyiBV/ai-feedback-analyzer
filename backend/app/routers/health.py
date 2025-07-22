"""Health check endpoint."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime

from app.database import get_async_session
from app.models.schemas import HealthResponse
from app.services.ai_service import OpenRouterClient

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(
    db: AsyncSession = Depends(get_async_session)
):
    """Check health status of the application."""
    
    # Check database connection
    db_status = "unhealthy"
    try:
        result = await db.execute(text("SELECT 1"))
        if result.scalar() == 1:
            db_status = "healthy"
    except Exception:
        pass
    
    # Check AI service
    ai_status = "unhealthy"
    try:
        async with OpenRouterClient() as ai_client:
            if await ai_client.check_health():
                ai_status = "healthy"
    except Exception:
        pass
    
    # Overall status
    overall_status = "healthy" if db_status == "healthy" and ai_status == "healthy" else "degraded"
    
    return HealthResponse(
        status=overall_status,
        database=db_status,
        ai_service=ai_status,
        timestamp=datetime.utcnow()
    )