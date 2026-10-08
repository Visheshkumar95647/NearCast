"""add activity location constraints and spatial index

Revision ID: fd2b3bbdfd41
Revises: f05c0ba2b64f
Create Date: 2026-09-25 14:10:58.304423

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "fd2b3bbdfd41"
down_revision: Union[str, Sequence[str], None] = "f05c0ba2b64f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_activity_location_activity",
        "activity_locations",
        ["activity_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_activity_location_activity",
        "activity_locations",
        type_="unique",
    )