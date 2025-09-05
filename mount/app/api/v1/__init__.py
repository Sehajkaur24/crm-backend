from fastapi import APIRouter

from app.api.v1 import event_api, lead_api, organisation_api, user_api
from app.api.v1 import opportunity_api

v1_router = APIRouter()

v1_router.include_router(user_api.router, prefix="/v1", tags=["User"])
v1_router.include_router(organisation_api.router, prefix="/v1", tags=["Organisation"])
v1_router.include_router(lead_api.router, prefix="/v1", tags=["Lead"])
v1_router.include_router(event_api.router, prefix="/v1", tags=["Event"])
v1_router.include_router(opportunity_api.router, prefix="/v1", tags=["Opportunity"])
