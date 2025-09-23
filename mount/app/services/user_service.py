from asyncpg import Connection

from app.exceptions.user_exception import (
    InvalidCredentialsException,
    UserAlreadyExistException,
    UserNotFoundException,
)
from app.repos.task_repo import TaskCreate, TaskUpdate, TaskRead, TaskRepo
from app.api.models.user_models import TokenResponse
from app.api.models.user_models import (
    AdminCreateRequest,
    TokenRequest,
    UpdateProfileRequest,
    ChangePasswordRequest
)
from app.repos.organisation_repo import OrganisationRepo, OrganisationCreate
from app.repos.user_repo import UserCreate, UserRepo, UserRead, UserType
from app.common.security import create_token, hash_password, verify_password




async def create_admin(conn: Connection, data: AdminCreateRequest) -> UserRead:
    org_repo = OrganisationRepo(conn)
    user_repo = UserRepo(conn)

    existing_user = await user_repo.get_by_email(email=data.email)
    if existing_user:
        raise UserAlreadyExistException(email=data.email)

    org = await org_repo.create_org(
        data=OrganisationCreate(name=data.org_name, industry=data.industry)
    )
    
    new_user = await user_repo.create_user(
        data=UserCreate(
            full_name=data.full_name,
            email=data.email,
            password_hash=hash_password(data.password),
            user_type=UserType.ADMIN,
            organisation_id=org.id,
        )
    )

    return new_user


async def sign_in(conn: Connection, data: TokenRequest) -> TokenResponse:
    user_repo = UserRepo(conn)
    user = await user_repo.get_by_email(email=data.email)
    if not user:
        raise UserNotFoundException(email=data.email)
    if not verify_password(password=data.password, password_hash=user.password_hash):
        raise InvalidCredentialsException()
    token = create_token(user_id=user.id)
    return TokenResponse(user=user, access_token=token)


async def create_user_task(conn: Connection, data: TaskCreate) -> TaskRead | None:
    task_repo = TaskRepo(conn)
    task = await task_repo.create_task(data=data)
    return task


async def update_user_task(
    conn: Connection, task_id: int, data: TaskUpdate
) -> TaskRead | None:
    task_repo = TaskRepo(conn)
    task = await task_repo.edit_task(task_id=task_id, data=data)
    return task


async def get_user_tasks(conn: Connection, user_id: int) -> list[TaskRead]:
    task_repo = TaskRepo(conn)
    tasks = await task_repo.get_user_tasks(user_id=user_id)
    return tasks


async def update_profile(conn: Connection, data: UpdateProfileRequest, user_id:int) ->  UserRead | None:
    user_repo=UserRepo(conn)
    user_repo= await user_repo.update_profile(full_name=data.full_name,email=data.email,user_id=user_id)
    return user_repo


async def change_password(conn: Connection, data: ChangePasswordRequest, user_id: int) -> UserRead:
    user_repo = UserRepo(conn)
    user = await user_repo.get_by_id(user_id=user_id)
    if not user:
        raise UserNotFoundException(f"User with id {user_id} not found.")

    if not verify_password(password=data.old_password, password_hash=user.password_hash):
        raise InvalidCredentialsException()

    hashed_new_password = hash_password(data.new_password)
    updated_user = await user_repo.change_password(
        user_id=user_id, new_password=hashed_new_password
    )
    return updated_user
