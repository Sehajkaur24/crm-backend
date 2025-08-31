from enum import Enum

from asyncpg import Connection
from pydantic import BaseModel

from app.common.base_models import DBBaseModel


class UserType(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"


class UserBase(BaseModel):
    full_name: str
    email: str
    password_hash: str
    user_type: UserType
    organisation_id: int


class UserRead(UserBase, DBBaseModel):
    pass


class UserCreate(UserBase):
    pass


class UserRepo:
    TABLE_NAME = "users"
    READ_PARAMS = """full_name, email, password_hash, user_type, organisation_id, id, created_at, updated_at"""

    def __init__(self, conn: Connection):
        self.conn = conn

    def _base_read(self) -> str:
        return f"SELECT {self.READ_PARAMS} FROM {self.TABLE_NAME}"

    async def create_user(self, data: UserCreate) -> UserRead:
        params = [
            data.full_name,
            data.email,
            data.password_hash,
            data.user_type.value,
            data.organisation_id,
        ]
        query = f"""
        INSERT INTO users (full_name, email, password_hash, user_type, organisation_id, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
        RETURNING {self.READ_PARAMS}
        """
        recs = await self.conn.fetch(query, *params)
        return UserRead(**recs[0])

    async def get_by_email(self, email: str) -> UserRead | None:
        query = self._base_read() + " WHERE email = $1"
        recs = await self.conn.fetch(query, email)
        return UserRead(**recs[0]) if recs else None

    async def get_org_employees(self, org_id: int) -> list[UserRead]:
        query = self._base_read() + " WHERE organisation_id = $1 AND user_type = $2"
        recs = await self.conn.fetch(query, org_id, UserType.EMPLOYEE.value)
        return [UserRead(**rec) for rec in recs]
