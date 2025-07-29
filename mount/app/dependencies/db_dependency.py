from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from fastapi.param_functions import Depends
from typing import Annotated


async def async_get_db(request: Request):
    """
    Dependency that provides an async database session.

    Args:
        request (Request): The FastAPI request object, which contains the application state.

    Yields:
        AsyncSession: An asynchronous database session.
    """
    async with AsyncSession(request.app.state.db_pool) as db:
        yield db
    

AsyncSessionDep = Annotated[AsyncSession, Depends(async_get_db)]