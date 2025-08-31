


from pydantic import BaseModel, Field
from datetime import date

class EventCreateRequest(BaseModel):
    title: str = Field(..., examples=["Event 1"])
    event_date: date = Field(..., examples=["2025-08-31"])
    location: str = Field(..., examples=["Location 1"])
    status: str = Field(..., examples=["scheduled", "completed", "cancelled"])