from pydantic import BaseModel, ConfigDict, Field
from app.schemas.base_schema import DBBaseModel


class UserRead(DBBaseModel):
    full_name: str
    email: str
    password_hash: str


class UserCreateRequest(BaseModel):
    email: str = Field(..., examples=['john@example.com'])
    password: str = Field(..., examples=['topsecret'])
    user_type: str = Field(default="employee", examples=['user'])


class UserCreateWithHash(BaseModel):
    full_name: str
    email: str
    password: str
    user_type: str = Field(default="employee")
    organisation_id: int


class TokenResponse(BaseModel):
    access_token: str
    user: UserRead

    model_config = ConfigDict(from_attributes=True)


class TokenRequest(BaseModel):
    email: str = Field(..., examples=['john@example.com'])
    password: str = Field(..., examples=['topsecret'])


class AdminCreateRequest(BaseModel):
    full_name: str = Field(..., examples=['John Doe'])
    email: str = Field(..., examples=['john@example.com'])
    password: str = Field(..., examples=['topsecret'])
    org_name: str = Field(..., examples=['My Organization'])
    industry: str = Field(..., examples=['IT'])
