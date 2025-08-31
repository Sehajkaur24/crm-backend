from asyncpg import Connection
from pydantic import BaseModel, ConfigDict

from app.common.base_models import DBBaseModel


class OrganisationBase(BaseModel):
    name: str
    industry: str


class OrganisationRead(OrganisationBase, DBBaseModel):
    model_config = ConfigDict(from_attributes=True)


class OrganisationCreate(OrganisationBase):
    pass


class OrganisationUpdate(OrganisationBase):
    pass


class OrganisationRepo:
    TABLE_NAME = "organisations"
    READ_PARAMS = """name, industry, id, created_at, updated_at"""

    def __init__(self, conn: Connection):
        self.conn = conn

    def _base_read(self) -> str:
        return f"SELECT {self.READ_PARAMS} FROM {self.TABLE_NAME}"

    async def create_org(self, data: OrganisationCreate) -> OrganisationRead:
        params = [data.name, data.industry]
        query = f"""
        INSERT INTO organisations (name, industry, created_at, updated_at)
        VALUES ($1, $2, NOW(), NOW())
        RETURNING {self.READ_PARAMS}
        """
        recs = await self.conn.fetch(query, *params)
        return OrganisationRead(**recs[0])
