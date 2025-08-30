from asyncpg import Connection
from pydantic import BaseModel, ConfigDict
from app.schemas.base_schema import DBBaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str
    user_id: int
    organisation_id: int


class TaskRead(TaskBase, DBBaseModel):
    model_config = ConfigDict(from_attributes=True)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskRepo:
    TABLE_NAME = "tasks"
    READ_PARAMS = """
    title, description, status, user_id, organisation_id, id, created_at, updated_at
    """

    def __init__(self, conn: Connection):
        self.conn = conn

    def _base_read(self) -> str:
        return f"SELECT {self.READ_PARAMS} FROM {self.TABLE_NAME}"

    async def create_task(self, data: TaskCreate) -> TaskRead | None:
        params = [
            data.title,
            data.description,
            data.status,
            data.user_id,
            data.organisation_id,
        ]
        query = f"""
        INSERT INTO tasks (title, description, status, user_id, organisation_id, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
        RETURNING {self.READ_PARAMS}
        """
        recs = await self.conn.fetch(query, *params)
        return TaskRead(**recs[0]) if recs else None

    async def edit_task(self, task_id: int, data: TaskUpdate) -> TaskRead | None:
        params = [
            data.title,
            data.description,
            data.status,
            data.user_id,
            data.organisation_id,
            task_id,
        ]
        query = f"""
        UPDATE tasks
        SET title = $1, description = $2, status = $3, user_id = $4, organisation_id = $5, updated_at = NOW()
        WHERE id = $6
        RETURNING {self.READ_PARAMS}
        """
        recs = await self.conn.fetch(query, *params)
        return TaskRead(**recs[0]) if recs else None

    async def get_all_tasks_by_org_id(self, org_id: int) -> list[TaskRead]:
        query = self._base_read() + " WHERE organisation_id = $1"
        recs = await self.conn.fetch(query, org_id)
        return [TaskRead(**rec) for rec in recs]

    async def get_user_tasks(self, user_id: int) -> list[TaskRead]:
        query = self._base_read() + " WHERE user_id = $1"
        recs = await self.conn.fetch(query, user_id)
        return [TaskRead(**rec) for rec in recs]
