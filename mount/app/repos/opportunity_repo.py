from asyncpg import Connection
from pydantic import BaseModel

from app.common.base_models import DBBaseModel


class OpportunityBase(BaseModel):
    title: str
    amount: str
    stage: str
    close_date: str
    organisation_id: int


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityUpdate(OpportunityBase):
    pass


class OpportunityRead(OpportunityBase, DBBaseModel):
    pass


class OpportunityRepo:
    TABLE_NAME = "opportunities"

    READ_PARAMS = """
    id,
    title,
    amount,
    stage,
    close_date,
    organisation_id,
    created_at,
    updated_at
    """

    def __init__(self, conn: Connection):
        self.conn = conn

    def _base_read(self) -> str:
        return f"SELECT {self.READ_PARAMS} FROM {self.TABLE_NAME}"

    async def create_opportunity(self, data: OpportunityCreate) -> OpportunityRead:
        query = f"""
        INSERT INTO opportunities (title, amount, stage, close_date, organisation_id, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
        RETURNING {self.READ_PARAMS}
        """
        rec = await self.conn.fetch(
            query,
            data.title,
            data.amount,
            data.stage,
            data.close_date,
            data.organisation_id,
        )
        return OpportunityRead(**rec[0])

    async def edit_opportunity(
        self, opportunity_id: int, data: OpportunityUpdate
    ) -> OpportunityRead | None:
        params = [
            data.title,
            data.amount,
            data.stage,
            data.close_date,
            data.organisation_id,
            opportunity_id,
        ]
        query = f"""
        UPDATE opportunities
        SET title = $1, amount = $2, stage = $3, close_date = $4, organisation_id = $5, updated_at = NOW()
        WHERE id = $6
        RETURNING {self.READ_PARAMS}
        """
        recs = await self.conn.fetch(query, *params)
        return OpportunityRead(**recs[0]) if recs else None

    async def get_by_org_id(self, org_id: int) -> list[OpportunityRead]:
        query = self._base_read() + " WHERE organisation_id = $1"
        recs = await self.conn.fetch(query, org_id)
        return [OpportunityRead(**rec) for rec in recs]
