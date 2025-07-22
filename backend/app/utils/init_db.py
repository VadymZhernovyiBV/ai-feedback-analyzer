"""Database initialization script."""
import asyncio
import logging
from sqlalchemy import text

from app.database import engine, init_db
from app.models import feedback  # Import models to register them

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_tables():
    """Create all database tables."""
    logger.info("Creating database tables...")
    await init_db()
    logger.info("Database tables created successfully!")


async def check_tables():
    """Check if tables exist."""
    async with engine.begin() as conn:
        # Check if feedback_entries table exists
        result = await conn.execute(
            text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='feedback_entries';
            """)
        )
        table_exists = result.scalar() is not None
        
        if table_exists:
            logger.info("Table 'feedback_entries' exists")
            
            # Get row count
            count_result = await conn.execute(
                text("SELECT COUNT(*) FROM feedback_entries")
            )
            count = count_result.scalar()
            logger.info(f"Total feedback entries: {count}")
        else:
            logger.warning("Table 'feedback_entries' does not exist")


if __name__ == "__main__":
    asyncio.run(create_tables())
    asyncio.run(check_tables())