from pydantic import BaseModel, Field


class LeadCreateRequest(BaseModel):
    name: str = Field(..., examples=["Lead name"])
    email: str | None = Field(None, examples=["lead@example.com"])
    phone: str | None = Field(None, examples=["1234567890"])
    status: str | None = Field(None, examples=["started", "in_progress", "completed", "failed"])
