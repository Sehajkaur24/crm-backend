from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.exceptions.user_exception import UserAlreadyExistException
from app.repositories.user_repository import user_repo
from app.schemas.user_schema import UserCreateRequest


async def create_user(db: AsyncSession, user: UserCreateRequest) -> User:
    existing_user = await user_repo.get_by_attribute(
        db=db, attribute="email", value=user.email
    )
    if existing_user:
        raise UserAlreadyExistException(email=user.email)

    return await user_repo.create_with_hash(db=db, obj=user)
