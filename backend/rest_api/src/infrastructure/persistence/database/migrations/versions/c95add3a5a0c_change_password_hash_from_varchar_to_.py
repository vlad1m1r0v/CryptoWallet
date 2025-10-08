"""change password_hash from varchar to bytes

Revision ID: c95add3a5a0c
Revises: 3cab488cac0f
Create Date: 2025-10-08 10:36:09.735651
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c95add3a5a0c'
down_revision: Union[str, Sequence[str], None] = '3cab488cac0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Увага: тут важливо додати USING
    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN password_hash
        TYPE BYTEA
        USING password_hash::bytea
        """
    )


def downgrade() -> None:
    # При поверненні назад можна просто привести назад до VARCHAR
    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN password_hash
        TYPE VARCHAR(255)
        USING encode(password_hash, 'escape')
        """
    )