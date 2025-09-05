from fastapi import APIRouter

from app.common import responses
from app.dependencies.db_dependency import DBConnectionDep
from app.repos.opportunity_repo import OpportunityRead, OpportunityUpdate
from app.services import opportunity_service


router = APIRouter()


@router.put(
    "/opportunities/{opportunity_id}",
    response_model=responses.ResponseModel[OpportunityRead],
)
async def update_opportunity(
    conn: DBConnectionDep, opportunity_id: int, data: OpportunityUpdate
):
    opportunity = await opportunity_service.edit_opportunity(
        conn=conn, opportunity_id=opportunity_id, data=data
    )
    return responses.success(data=opportunity)
