


from fastapi import APIRouter
from app.common import responses
from app.schemas.lead_schema import LeadRead, LeadUpdate
from app.dependencies.db_dependency import AsyncSessionDep
from app.services import lead_service


router = APIRouter()


@router.put(
    "/leads/{lead_id}", response_model=responses.ResponseModel[LeadRead]
)
async def update_lead(db: AsyncSessionDep, lead_id: int, data: LeadUpdate):
    lead = await lead_service.edit_lead(db=db, lead_id=lead_id, data=data)
    return responses.success(data=lead)
