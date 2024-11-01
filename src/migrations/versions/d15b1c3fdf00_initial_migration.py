"""initial migration

Revision ID: d15b1c3fdf00
Revises: a9cba6cd52ab
Create Date: 2024-10-27 01:07:50.328523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd15b1c3fdf00'
down_revision: Union[str, None] = 'a9cba6cd52ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
