from asyncpg import Connection
from app.repos.event_repo import EventCreate, EventRead, EventRepo
from app.api.models.event_model import EventCreateRequest


async def create_event(
    conn: Connection, org_id: int, data: EventCreateRequest
) -> EventRead | None:
    event_repo = EventRepo(conn)
    event = await event_repo.create_event(
        data=EventCreate(
            title=data.title,
            date=data.event_date,
            location=data.location,
            status=data.status,
            organisation_id=org_id,
        )
    )
    return event


async def get_events_by_org_id(conn: Connection, org_id: int) -> list[EventRead]:
    event_repo = EventRepo(conn)
    events = await event_repo.get_events_by_org_id(org_id=org_id)
    return events
