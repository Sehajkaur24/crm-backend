from asyncpg import Connection

from app.exceptions.user_exception import UserAlreadyExistException
from app.repos.task_repo import TaskRepo
from app.repos.user_repo import UserRepo, UserRead, UserCreate, UserType
from app.api.models.user_models import EmployeeCreateRequest
from app.repos.task_repo import TaskRead
from app.common.security import hash_password


async def add_user_to_organisation(
    conn: Connection, org_id: int, data: EmployeeCreateRequest
) -> UserRead:
    user_repo = UserRepo(conn=conn)
    existing_user = await user_repo.get_by_email(email=data.email)
    if existing_user:
        raise UserAlreadyExistException(email=data.email)

    user = await user_repo.create_user(
        data=UserCreate(
            full_name=data.full_name,
            email=data.email,
            password_hash=hash_password(data.password),
            user_type=UserType.EMPLOYEE,
            organisation_id=org_id,
        ),
    )

    return user


async def get_organisation_users(conn: Connection, org_id: int) -> list[UserRead]:
    user_repo = UserRepo(conn=conn)
    users = await user_repo.get_org_employees(org_id=org_id)
    return users


async def get_organisation_tasks(conn: Connection,org_id: int) -> list[TaskRead]:
    task_repo = TaskRepo(conn=conn)
    tasks = await task_repo.get_all_tasks_by_org_id(org_id=org_id)
    return tasks
