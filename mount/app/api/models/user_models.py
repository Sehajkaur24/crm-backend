from pydantic import BaseModel, Field

from app.repos.user_repo import UserRead


class TokenResponse(BaseModel):
    access_token: str
    user: UserRead


class UserCreateRequest(BaseModel):
    email: str = Field(..., examples=["john@example.com"])
    password: str = Field(..., examples=["topsecret"])
    user_type: str = Field(default="employee", examples=["user"])


class EmployeeCreateRequest(BaseModel):
    full_name: str = Field(..., examples=["John Doe"])
    email: str = Field(..., examples=["john@example.com"])
    password: str = Field(..., examples=["topsecret"])


class UserCreateWithHash(BaseModel):
    full_name: str
    email: str
    password: str
    user_type: str = Field(default="employee")
    organisation_id: int


class TokenRequest(BaseModel):
    email: str = Field(..., examples=["john@example.com"])
    password: str = Field(..., examples=["topsecret"])


class AdminCreateRequest(BaseModel):
    full_name: str = Field(..., examples=["John Doe"])
    email: str = Field(..., examples=["john@example.com"])
    password: str = Field(..., examples=["topsecret"])
    org_name: str = Field(..., examples=["My Organization"])
    industry: str = Field(..., examples=["IT"])
