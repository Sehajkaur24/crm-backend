

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import user_repo
from app.schemas.user_schema import EmployeeCreateRequest, UserCreateWithHash, UserRead
from app.exceptions.user_exception import UserAlreadyExistException


async def add_user_to_organisation(db: AsyncSession, org_id: int, data: EmployeeCreateRequest) -> UserRead:
    existing_user = await user_repo.get_by_attribute(db=db, attribute="email", value=data.email)
    if existing_user:
        raise UserAlreadyExistException(email=data.email)

    user = await user_repo.create_with_hash(db=db, obj=UserCreateWithHash(
        full_name=data.full_name,
        email=data.email,
        password=data.password,
        user_type="employee",
        organisation_id=org_id,
    ))

    return UserRead.model_validate(user)