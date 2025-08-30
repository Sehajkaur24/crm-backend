from asyncpg import Connection
from pydantic import BaseModel
from app.schemas.base_schema import DBBaseModel
from pydantic import ConfigDict


class LeadBase(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    status: str | None = None
    organisation_id: int


class LeadCreate(LeadBase):
    pass


class LeadUpdate(LeadBase):
    pass


class LeadRead(LeadBase, DBBaseModel):
    model_config = ConfigDict(from_attributes=True)


class LeadRepo:
    TABLE_NAME = "leads"

    READ_PARAMS = """
    name, email, phone, status, organisation_id, id, created_at, updated_at
    """

    def __init__(self, conn: Connection):
        self.conn = conn

    def _base_read(self) -> str:
        return f"SELECT {self.READ_PARAMS} FROM {self.TABLE_NAME}"

    async def get_all_leads_by_org_id(self, org_id: int) -> list[LeadRead]:
        query = self._base_read() + " WHERE organisation_id = $1"
        recs = await self.conn.fetch(query, org_id)
        return [LeadRead(**rec) for rec in recs]

    async def create_lead(self, data: LeadCreate) -> LeadRead | None:
        params = [data.name, data.email, data.phone, data.status, data.organisation_id]
        query = f"""
        INSERT INTO leads (name, email, phone, status, organisation_id, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
        RETURNING {self.READ_PARAMS}
        """
        recs = await self.conn.fetch(query, *params)
        return LeadRead(**recs[0]) if recs else None

    async def edit_lead(self, lead_id: int, data: LeadUpdate) -> LeadRead | None:
        params = [
            data.name,
            data.email,
            data.phone,
            data.status,
            data.organisation_id,
            lead_id,
        ]
        query = f"""
        UPDATE leads
        SET name = $1, email = $2, phone = $3, status = $4, organisation_id = $5, updated_at = NOW()
        WHERE id = $6
        RETURNING {self.READ_PARAMS}
        """
        recs = await self.conn.fetch(query, *params)
        return LeadRead(**recs[0]) if recs else None
