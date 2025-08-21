from pydantic import BaseModel
from app.schemas.base_schema import DBBaseModel
from pydantic import ConfigDict, Field


class LeadBase(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    status: str | None = None
    organisation_id: int


class LeadCreate(LeadBase):
    pass


class LeadUpdate(LeadBase):
    pass


class LeadRead(LeadBase, DBBaseModel):
    model_config = ConfigDict(from_attributes=True)


class LeadCreateRequest(BaseModel):
    name: str = Field(..., examples=["Lead name"])
    email: str | None = Field(None, examples=["lead@example.com"])
    phone: str | None = Field(None, examples=["1234567890"])
    status: str | None = Field(None, examples=["Lead status"])