from fastapi import APIRouter
from app.api.v1 import user_api, organisation_api, lead_api

v1_router = APIRouter()

v1_router.include_router(user_api.router, prefix="/v1", tags=["User"])
v1_router.include_router(organisation_api.router, prefix="/v1", tags=["Organisation"])
v1_router.include_router(lead_api.router, prefix="/v1", tags=["Lead"])
