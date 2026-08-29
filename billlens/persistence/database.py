"""
Database connection and session management.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from .models import Base


class Database:
    """
    Async database manager.
    """
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_async_engine(
            database_url,
            echo=False,
            future=True,
        )
        self.SessionLocal = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    
    async def connect(self) -> None:
        """Create all tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def disconnect(self) -> None:
        """Close engine."""
        await self.engine.dispose()
    
    async def get_session(self) -> AsyncSession:
        """Get a database session."""
        return self.SessionLocal()