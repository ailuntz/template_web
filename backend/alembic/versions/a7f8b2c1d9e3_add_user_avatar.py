"""Add user avatar

Revision ID: a7f8b2c1d9e3
Revises: 6ac8c40b709b
Create Date: 2025-12-09 23:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7f8b2c1d9e3'
down_revision: Union[str, None] = '6ac8c40b709b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('avatar', sa.String(length=500), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'avatar')
