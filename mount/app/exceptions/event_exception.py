from app.exceptions.base_exception import AppBaseException
from fastapi import status

class EventException(AppBaseException):
    def __init__(self, event_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="EVENT_NOT_FOUND",
            detail=f"Event with id {event_id} not found",
        )