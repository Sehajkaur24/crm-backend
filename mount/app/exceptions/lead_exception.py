from fastapi import status

from app.exceptions.base_exception import AppBaseException


class LeadNotFoundException(AppBaseException):
    def __init__(self, lead_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="LEAD_NOT_FOUND",
            detail=f"Lead with id {lead_id} not found",
        )
