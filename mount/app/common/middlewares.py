from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.common.settings import settings
from app.common.logger import logger

def init_middlewares(app: FastAPI):
    """
    Initialize all middlewares
    NOTE: All middlewares will run in order from top to bottom

    Args:
        app (FastAPI): FastAPI app instance
    """

    @app.middleware("http")
    async def request_logging(request: Request, call_next):
        logger.info(f"{request.method} {request.url}")
        response = await call_next(request)
        return response
    
    if settings.crm_environment == "dev":
        # Allow all origins in development
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        # Use specific allowed origins in production/staging
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_origins,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["*"],
        )