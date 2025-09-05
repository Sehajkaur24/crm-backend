from asyncpg import Connection

from app.api.models.opportunity_model import OpportunityCreateRequest
from app.repos.opportunity_repo import (
    OpportunityCreate,
    OpportunityRead,
    OpportunityRepo,
    OpportunityUpdate,
)


async def create_opportunity(
    conn: Connection, org_id: int, data: OpportunityCreateRequest
) -> OpportunityRead:
    op_repo = OpportunityRepo(conn=conn)

    return await op_repo.create_opportunity(
        data=OpportunityCreate(
            title=data.title,
            amount=data.amount,
            stage=data.stage,
            close_date=data.close_date,
            organisation_id=org_id,
        )
    )


async def edit_opportunity(
    conn: Connection, opportunity_id: int, data: OpportunityUpdate
) -> OpportunityRead | None:
    op_repo = OpportunityRepo(conn=conn)
    return await op_repo.edit_opportunity(opportunity_id=opportunity_id, data=data)


async def get_by_org_id(conn: Connection, org_id: int) -> list[OpportunityRead]:
    op_repo = OpportunityRepo(conn=conn)
    return await op_repo.get_by_org_id(org_id=org_id)
