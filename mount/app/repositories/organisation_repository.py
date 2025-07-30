from app.repositories.base_repository import BaseRepository
from app.database.models.organisation import Organisation

class OrganisationRepository(BaseRepository[Organisation]):
    pass

organisation_repo = OrganisationRepository(Organisation)
