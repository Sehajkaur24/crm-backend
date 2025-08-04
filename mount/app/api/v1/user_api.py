from fastapi import APIRouter, status

from app.common import responses
from app.dependencies.db_dependency import AsyncSessionDep
from app.schemas.user_schema import (
    AdminCreateRequest,
    TokenRequest,
    TokenResponse,
    UserRead,
)
from app.services import user_service

router = APIRouter()


@router.post("/auth/sign-in", response_model=responses.ResponseModel[TokenResponse])
async def sign_in(db: AsyncSessionDep, data: TokenRequest):
    res = await user_service.sign_in(db=db, data=data)
    return responses.success(data=res)


@router.post(
    "/users/create-admin",
    response_model=responses.ResponseModel[UserRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_admin(db: AsyncSessionDep, data: AdminCreateRequest):
    user = await user_service.create_admin(db=db, data=data)
    return responses.success(data=user)