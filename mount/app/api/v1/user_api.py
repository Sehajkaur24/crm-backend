from fastapi import APIRouter, status

from app.common import responses
from app.dependencies.db_dependency import AsyncSessionDep, DBConnectionDep
from app.schemas.user_schema import (
    AdminCreateRequest,
    TokenRequest,
    TokenResponse,
    UserRead,
)
from app.repos.task_repo import TaskCreate, TaskRead, TaskUpdate
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


@router.post(
    "/users/create-task",
    response_model=responses.ResponseModel[TaskRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_user_task(conn: DBConnectionDep, data: TaskCreate):
    task = await user_service.create_user_task(conn=conn, data=data)
    return responses.success(data=task)


@router.get(
    "/users/{user_id}/tasks", response_model=responses.ResponseModel[list[TaskRead]]
)
async def get_user_tasks(conn: DBConnectionDep, user_id: int):
    tasks = await user_service.get_user_tasks(conn=conn, user_id=user_id)
    return responses.success(data=tasks)


@router.put("/users/{task_id}/tasks", response_model=responses.ResponseModel[TaskRead])
async def update_user_task(conn: DBConnectionDep, task_id: int, data: TaskUpdate):
    task = await user_service.update_user_task(conn=conn, task_id=task_id, data=data)
    return responses.success(data=task)
