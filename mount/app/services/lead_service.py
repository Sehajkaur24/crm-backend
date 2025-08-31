from asyncpg import Connection

from app.repos.lead_repo import LeadRepo, LeadCreate, LeadRead, LeadUpdate
from app.api.models.lead_models import LeadCreateRequest
from app.exceptions.lead_exception import LeadNotFoundException


async def add_lead(
    conn: Connection, org_id: int, data: LeadCreateRequest
) -> LeadRead | None:
    lead_repo = LeadRepo(conn)
    lead = await lead_repo.create_lead(
        data=LeadCreate(
            name=data.name,
            email=data.email,
            phone=data.phone,
            status=data.status,
            organisation_id=org_id,
        ),
    )

    return lead


async def get_organisation_leads(conn: Connection, org_id: int) -> list[LeadRead]:
    lead_repo = LeadRepo(conn)

    leads = await lead_repo.get_all_leads_by_org_id(org_id=org_id)
    return leads


async def edit_lead(conn: Connection, lead_id: int, data: LeadUpdate) -> LeadRead:
    lead_repo = LeadRepo(conn)
    lead = await lead_repo.edit_lead(lead_id=lead_id, data=data)
    if not lead:
        raise LeadNotFoundException(lead_id=lead_id)
    return lead
