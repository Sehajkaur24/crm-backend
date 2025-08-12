from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.exceptions.user_exception import (
    InvalidCredentialsException,
    UserAlreadyExistException,
    UserNotFoundException,
)
from app.repositories.organisation_repository import organisation_repo
from app.repositories.user_repository import user_repo
from app.schemas.organisation_schema import OrganisationCreate
from app.schemas.user_schema import (
    AdminCreateRequest,
    TokenRequest,
    TokenResponse,
    UserCreateWithHash,
    UserRead,
)
from app.schemas.task_schema import TaskCreate, TaskRead
from app.repositories.task_repository import task_repo


async def create_admin(db: AsyncSession, data: AdminCreateRequest) -> User:
    existing_user = await user_repo.get_by_attribute(
        db=db, attribute="email", value=data.email
    )
    if existing_user:
        raise UserAlreadyExistException(email=data.email)

    org = await organisation_repo.create(
        db=db, obj_in=OrganisationCreate(name=data.org_name, industry=data.industry)
    )

    return await user_repo.create_with_hash(
        db=db,
        obj=UserCreateWithHash(
            full_name=data.full_name,
            email=data.email,
            password=data.password,
            user_type="admin",
            organisation_id=org.id,
        ),
    )


async def sign_in(db: AsyncSession, data: TokenRequest) -> TokenResponse:
    user = await user_repo.get_by_attribute(db=db, attribute="email", value=data.email)
    if not user:
        raise UserNotFoundException(email=data.email)
    if not user.verify_password(data.password):
        raise InvalidCredentialsException()
    return TokenResponse(user=UserRead.model_validate(user), access_token=user.token)


async def create_user_task(db: AsyncSession, data: TaskCreate) -> TaskRead:
    user = await user_repo.get_by_attribute(db=db, attribute="id", value=data.user_id)
    if not user:
        raise UserNotFoundException(email=str(data.user_id))
    task = await task_repo.create(db=db, obj_in=data)

    return TaskRead.model_validate(task)

async def update_user_task(db: AsyncSession, task_id: int, data: TaskCreate) -> TaskRead:
    task = await task_repo.update_by_id(db=db, id=task_id, obj_in=data)
    return TaskRead.model_validate(task)

async def get_user_tasks(db: AsyncSession, user_id: int) -> list[TaskRead]:
    tasks = await task_repo.get_multi_by_attribute(db=db, attribute="user_id", value=user_id)
    if not tasks:
        return []
    return [TaskRead.model_validate(task) for task in tasks]