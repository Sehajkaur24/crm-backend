from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.core import Base


class Organisation(Base):
    __tablename__ = "organisations"

    name: Mapped[str] = mapped_column(String)
    industry: Mapped[str] = mapped_column(String)
