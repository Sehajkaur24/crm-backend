
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base_schema import DBBaseModel

class TaskBase(BaseModel):
    title: str = Field(..., examples=["Task title"])
    description: str | None = Field(None, examples=["Task description"])
    status: str = Field(..., examples=["pending", "in_progress", "completed"])
    user_id: int = Field(..., examples=[1])
    organisation_id: int = Field(..., examples=[1])


class TaskRead(TaskBase,DBBaseModel):
    
    model_config = ConfigDict(from_attributes=True)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass
