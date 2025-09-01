from asyncpg import Connection
from app.common.base_models import DBBaseModel
from datetime import date
from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    location: str
    status: str
    organisation_id: int
    date: date


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventRead(EventBase, DBBaseModel):
    pass


class EventRepo:
    TABLE_NAME = "events"
    READ_PARAMS = (
        """title, date, location, status, organisation_id, id, created_at, updated_at"""
    )

    def __init__(self, conn: Connection):
        self.conn = conn
    
    def _base_read(self) -> str:
        return f"SELECT {self.READ_PARAMS} FROM {self.TABLE_NAME}"

    
    async def create_event(self, data: EventCreate) -> EventRead | None:
        params = [data.title, data.date, data.location, data.status, data.organisation_id]
        query = f"""
        INSERT INTO events (title, date, location, status, organisation_id, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
        RETURNING {self.READ_PARAMS}
        """
        recs = await self.conn.fetch(query, *params)
        return EventRead(**recs[0]) if recs else None
    
    async def edit_event(self, event_id: int, data: EventUpdate) -> EventRead | None:
        params = [data.title, data.date, data.location, data.status, data.organisation_id, event_id]
        query = f"""
        UPDATE events
        SET title = $1, date = $2, location = $3, status = $4, organisation_id = $5, updated_at = NOW()
        WHERE id = $6
        RETURNING {self.READ_PARAMS}
        """
        recs = await self.conn.fetch(query, *params)
        return EventRead(**recs[0]) if recs else None
    
    async def get_events_by_org_id(self, org_id: int) -> list[EventRead]:
        query = self._base_read() + " WHERE organisation_id = $1"
        recs = await self.conn.fetch(query, org_id)
        return [EventRead(**rec) for rec in recs]