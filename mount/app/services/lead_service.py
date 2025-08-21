
from app.repositories.lead_repository import lead_repo
from app.schemas.lead_schema import LeadCreateRequest, LeadRead, LeadCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def add_lead(db: AsyncSession, org_id: int, data: LeadCreateRequest) -> LeadRead:

    lead = await lead_repo.create(
        db=db,
        obj_in=LeadCreate(
            name=data.name,
            email=data.email,
            phone=data.phone,
            status=data.status,
            organisation_id=org_id,
        ),
    )

    return LeadRead.model_validate(lead)


async def get_organisation_leads(db: AsyncSession, org_id: int) -> list[LeadRead]:
    leads = await lead_repo.filter_by(
        db=db,
        filters={"organisation_id": org_id},
    )
    return [LeadRead.model_validate(lead) for lead in leads]
