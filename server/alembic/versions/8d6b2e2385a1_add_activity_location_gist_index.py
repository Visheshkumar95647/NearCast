"""add activity location gist index

Revision ID: 8d6b2e2385a1
Revises: fd2b3bbdfd41
Create Date: 2026-09-25 14:16:12.693570

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "8d6b2e2385a1"
down_revision: Union[str, Sequence[str], None] = "fd2b3bbdfd41"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_activity_locations_location_gist",
        "activity_locations",
        ["location"],
        unique=False,
        postgresql_using="gist",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_activity_locations_location_gist",
        table_name="activity_locations",
    )