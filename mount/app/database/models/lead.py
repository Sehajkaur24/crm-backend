from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.core import Base


class Lead(Base):
    __tablename__ = "leads"

    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str | None] = mapped_column(String)
    phone: Mapped[str | None] = mapped_column(String)
    status: Mapped[str | None] = mapped_column(String)
    organisation_id: Mapped[int] = mapped_column(
        ForeignKey("organisations.id"), nullable=False
    )
