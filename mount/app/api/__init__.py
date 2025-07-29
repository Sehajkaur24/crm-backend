from fastapi import APIRouter
from app.api.v1 import v1_router


global_router = APIRouter()

global_router.include_router(v1_router)
