"""Import all routers."""
from app.routers.feedback import router as feedback_router
from app.routers.analytics import router as analytics_router
from app.routers.health import router as health_router

__all__ = ["feedback_router", "analytics_router", "health_router"]