from pydantic import BaseModel, Field


class OpportunityCreateRequest(BaseModel):
    title: str = Field(..., examples=["Opportunity 1"])
    amount: str = Field(..., examples=["1000"])
    stage: str = Field(..., examples=["Stage 1"])
    close_date: str = Field(..., examples=["2025-09-05"])
