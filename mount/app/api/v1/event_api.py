from fastapi import APIRouter

from app.common import responses
from app.repos.event_repo import EventRead, EventUpdate
from app.services import event_service
from app.dependencies.db_dependency import DBConnectionDep

router = APIRouter()


@router.put("/events/{event_id}", response_model=responses.ResponseModel[EventRead])
async def update_event(conn: DBConnectionDep, event_id: int, data: EventUpdate):
    event = await event_service.edit_event(conn=conn, event_id=event_id, data=data)
    return responses.success(data=event)
