from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.repositories.base_repository import BaseRepository
from app.schemas.user_schema import UserCreateWithHash


class UserRepository(BaseRepository[User]):
    async def create_with_hash(
        self, db: AsyncSession, *, obj: UserCreateWithHash
    ) -> User:
        user_obj = User()
        user_obj.full_name = obj.full_name
        user_obj.email = obj.email
        user_obj.set_password(obj.password)
        user_obj.user_type = obj.user_type
        user_obj.organisation_id = obj.organisation_id

        db.add(user_obj)

        await db.commit()
        await db.refresh(user_obj)

        return user_obj


user_repo = UserRepository(User)
