from typing import Annotated

import asyncpg
from fastapi import Request
from fastapi.param_functions import Depends


async def get_db_connection(request: Request):
    async with request.app.state.pg_pool.acquire() as conn:
        yield conn


DBConnectionDep = Annotated[asyncpg.connection.Connection, Depends(get_db_connection)]
