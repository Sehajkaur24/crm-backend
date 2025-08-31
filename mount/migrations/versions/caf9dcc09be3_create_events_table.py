"""create_events_table

Revision ID: caf9dcc09be3
Revises: 8e4fdc0ec34f
Create Date: 2025-08-31 19:53:38.029692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'caf9dcc09be3'
down_revision: Union[str, Sequence[str], None] = '8e4fdc0ec34f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('events',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('organisation_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['organisation_id'], ['organisations.id'], "events_organisation_id_fkey"),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_constraint('events_organisation_id_fkey', 'events', type_='foreignkey')
    op.drop_table('events')