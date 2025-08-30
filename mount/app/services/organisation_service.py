from asyncpg import Connection
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.exceptions.user_exception import UserAlreadyExistException
from app.repos.task_repo import TaskRepo
from app.repositories.user_repository import user_repo
from app.schemas.user_schema import EmployeeCreateRequest, UserCreateWithHash, UserRead
from app.repos.task_repo import TaskRead


async def add_user_to_organisation(
    db: AsyncSession, org_id: int, data: EmployeeCreateRequest
) -> UserRead:
    existing_user = await user_repo.get_by_attribute(
        db=db, attribute="email", value=data.email
    )
    if existing_user:
        raise UserAlreadyExistException(email=data.email)

    user = await user_repo.create_with_hash(
        db=db,
        obj=UserCreateWithHash(
            full_name=data.full_name,
            email=data.email,
            password=data.password,
            user_type="employee",
            organisation_id=org_id,
        ),
    )

    return UserRead.model_validate(user)


async def get_organisation_users(db: AsyncSession, org_id: int) -> list[User]:
    users = await user_repo.filter_by(
        db=db,
        filters={"organisation_id": org_id, "user_type": "employee"},
    )
    return users


async def get_organisation_tasks(conn: Connection,org_id: int) -> list[TaskRead]:
    task_repo = TaskRepo(conn=conn)
    tasks = await task_repo.get_all_tasks_by_org_id(org_id=org_id)
    return tasks
