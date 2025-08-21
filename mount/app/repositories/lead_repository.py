from app.repositories.base_repository import BaseRepository
from app.database.models.lead import Lead


class LeadRepository(BaseRepository[Lead]):
    pass


lead_repo = LeadRepository(Lead)
