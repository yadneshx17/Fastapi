"""add user table

Revision ID: e2fe58ec1fe8
Revises: 2f29db94a7fb
Create Date: 2024-12-14 22:59:36.461145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2fe58ec1fe8'
down_revision: Union[str, None] = '2f29db94a7fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                sa.Column('id', sa. Integer(),nullable=False),
                sa.Column('email', sa.String(), nullable=False),
                sa.Column('password', sa. String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP (timezone=True), server_default=sa.text('now()'), nullable=False),
                sa. PrimaryKeyConstraint('id'),
                sa. UniqueConstraint('email')
                )
    pass

def downgrade() -> None:
    op.drop_table('users')
    pass