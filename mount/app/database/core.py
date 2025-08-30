from datetime import datetime, timezone
import asyncpg

from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.common.settings import settings

async def get_connection_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(settings.db_dsn)

def get_db_engine() -> AsyncEngine:
    """Create an async SQLAlchemy engine from the configured database URL.

    Returns:
        AsyncEngine: An async SQLAlchemy engine.
    """
    return create_async_engine(settings.db_url)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.

    This class contains common fields and behaviors that are shared by all
    SQLAlchemy models in the application.

    Attributes:
        id (int): The primary key of the model.
        created_at (datetime): A timestamp representing when the model was
            created.
        updated_at (datetime): A timestamp representing when the model was last
            updated.
    """
    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

