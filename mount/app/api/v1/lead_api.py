from fastapi import APIRouter

from app.common import responses
from app.dependencies.db_dependency import DBConnectionDep
from app.repos.lead_repo import LeadRead, LeadUpdate
from app.services import lead_service


router = APIRouter()


@router.put("/leads/{lead_id}", response_model=responses.ResponseModel[LeadRead])
async def update_lead(conn: DBConnectionDep, lead_id: int, data: LeadUpdate):
    lead = await lead_service.edit_lead(conn=conn, lead_id=lead_id, data=data)
    return responses.success(data=lead)
