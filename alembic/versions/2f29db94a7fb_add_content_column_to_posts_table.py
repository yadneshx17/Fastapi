"""add content column to posts table

Revision ID: 2f29db94a7fb
Revises: 992ffed1efd1
Create Date: 2024-12-14 22:55:36.459053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f29db94a7fb'
down_revision: Union[str, None] = '992ffed1efd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass