"""email unique

Revision ID: 69d8a6614ac6
Revises: 96f80ce5dcc4
Create Date: 2024-11-01 23:08:30.209850

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "69d8a6614ac6"
down_revision: Union[str, None] = "96f80ce5dcc4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")

