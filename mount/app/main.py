from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import global_router
from app.common.middlewares import init_middlewares
from app.common.exception_handlers import init_exception_middlewares
from app.database.core import get_db_engine

app_description = """
A FastAPI-powered backend.
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = get_db_engine()
    yield
    await app.state.db_pool.dispose()


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
