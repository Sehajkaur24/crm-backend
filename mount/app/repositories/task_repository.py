from app.repositories.base_repository import BaseRepository
from app.database.models.task import Task


class TaskRepository(BaseRepository[Task]):
    pass


task_repo = TaskRepository(Task)
