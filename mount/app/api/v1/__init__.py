from fastapi import APIRouter
from app.api.v1 import user_api

v1_router = APIRouter()

v1_router.include_router(user_api.router, prefix="/v1")
