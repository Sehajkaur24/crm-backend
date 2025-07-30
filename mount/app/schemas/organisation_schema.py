


from app.schemas.base_schema import DBBaseModel
from pydantic import BaseModel


class OrganisationBase(BaseModel):
    name: str
    industry: str


class OrganisationRead(DBBaseModel, OrganisationBase):
    pass


class OrganisationCreate(OrganisationBase):
    pass


class OrganisationUpdate(OrganisationBase):
    pass
