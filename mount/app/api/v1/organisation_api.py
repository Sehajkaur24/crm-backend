from fastapi import APIRouter

from app.api.models.lead_models import LeadCreateRequest
from app.api.models.user_models import EmployeeCreateRequest
from app.common import responses
from app.dependencies.db_dependency import DBConnectionDep
from app.repos.lead_repo import LeadRead
from app.repos.task_repo import TaskRead
from app.repos.user_repo import UserRead
from app.services import lead_service, organisation_service

router = APIRouter()


@router.post(
    "/organisations/{org_id}/users", response_model=responses.ResponseModel[UserRead]
)
async def add_user_to_organisation(
    data: EmployeeCreateRequest, conn: DBConnectionDep, org_id: int
):
    res = await organisation_service.add_user_to_organisation(
        conn=conn, org_id=org_id, data=data
    )
    return responses.success(data=res)


@router.get(
    "/organisations/{org_id}/users",
    response_model=responses.ResponseModel[list[UserRead]],
)
async def get_organisation_users(conn: DBConnectionDep, org_id: int):
    res = await organisation_service.get_organisation_users(conn=conn, org_id=org_id)
    return responses.success(data=res)


@router.get(
    "/organisations/{org_id}/tasks",
    response_model=responses.ResponseModel[list[TaskRead]],
)
async def get_organisation_tasks(org_id: int, conn: DBConnectionDep):
    res = await organisation_service.get_organisation_tasks(org_id=org_id, conn=conn)
    return responses.success(data=res)


@router.post(
    "/organisations/{org_id}/leads", response_model=responses.ResponseModel[LeadRead]
)
async def add_lead_to_organisation(
    data: LeadCreateRequest, conn: DBConnectionDep, org_id: int
):
    res = await lead_service.add_lead(conn=conn, org_id=org_id, data=data)
    return responses.success(data=res)


@router.get(
    "/organisations/{org_id}/leads",
    response_model=responses.ResponseModel[list[LeadRead]],
)
async def get_organisation_leads(org_id: int, conn: DBConnectionDep):
    res = await lead_service.get_organisation_leads(conn=conn, org_id=org_id)
    return responses.success(data=res)
