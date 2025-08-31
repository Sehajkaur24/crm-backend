from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import global_router
from app.common.middlewares import init_middlewares
from app.common.exception_handlers import init_exception_middlewares
from app.database.core import get_connection_pool

app_description = """
A FastAPI-powered backend.
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pg_pool = await get_connection_pool()
    yield
    await app.state.pg_pool.close()


app = FastAPI(
    title="CRM API",
    description=app_description,
    version="1.0.0",
    lifespan=lifespan,
)

init_middlewares(app)
init_exception_middlewares(app)

app.include_router(global_router)


@app.get("/", tags=["Health Check"])
def health_check():
    return {"health": "ok"}
