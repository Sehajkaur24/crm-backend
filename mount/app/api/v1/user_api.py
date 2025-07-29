from fastapi import APIRouter, status

from app.common import responses
from app.dependencies.db_dependency import AsyncSessionDep
from app.schemas.user_schema import UserCreateRequest, UserRead
from app.services import user_service

router = APIRouter()


@router.post(
    "/users",
    response_model=responses.ResponseModel[UserRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(db: AsyncSessionDep, data: UserCreateRequest):
    user = await user_service.create_user(db=db, user=data)
    return responses.success(data=user)
