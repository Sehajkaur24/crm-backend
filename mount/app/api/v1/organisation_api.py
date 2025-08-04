from fastapi import APIRouter

from app.dependencies.db_dependency import AsyncSessionDep
from app.schemas.user_schema import EmployeeCreateRequest, UserRead
from app.common import responses
from app.services import organisation_service

router = APIRouter()


@router.post("/organisations/{org_id}/users", response_model=responses.ResponseModel[UserRead])
async def add_user_to_organisation(
    data: EmployeeCreateRequest, db: AsyncSessionDep, org_id: int
):
    res = await organisation_service.add_user_to_organisation(db=db, org_id=org_id, data=data)
    return responses.success(data=res)
