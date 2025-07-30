from fastapi import APIRouter, status

from app.common import responses
from app.dependencies.db_dependency import AsyncSessionDep
from app.schemas.user_schema import AdminCreateRequest, UserRead
from app.services import user_service

router = APIRouter()


@router.post(
    "/users/create-admin",
    response_model=responses.ResponseModel[UserRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_admin(db: AsyncSessionDep, data: AdminCreateRequest):
    user = await user_service.create_admin(db=db, data=data)
    return responses.success(data=user)
