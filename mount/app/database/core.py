import asyncpg

from app.common.settings import settings

async def get_connection_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(settings.db_dsn)
