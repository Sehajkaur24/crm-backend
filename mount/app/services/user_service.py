from app.database.models.user import User
from app.exceptions.user_exception import UserAlreadyExistException
from app.repositories.organisation_repository import organisation_repo
from app.repositories.user_repository import user_repo
from app.schemas.organisation_schema import OrganisationCreate
from app.schemas.user_schema import AdminCreateRequest, UserCreateWithHash
from sqlalchemy.ext.asyncio import AsyncSession


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
