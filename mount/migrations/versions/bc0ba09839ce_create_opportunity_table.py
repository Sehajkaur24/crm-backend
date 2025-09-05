"""create_opportunity_table

Revision ID: bc0ba09839ce
Revises: caf9dcc09be3
Create Date: 2025-09-05 16:16:15.269556

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bc0ba09839ce"
down_revision: Union[str, Sequence[str], None] = "caf9dcc09be3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "opportunities",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("amount", sa.String(), nullable=True),
        sa.Column("stage", sa.String(), nullable=True),
        sa.Column("close_date", sa.String(), nullable=True),
        sa.Column("organisation_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["organisation_id"],
            ["organisations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("opportunities")
