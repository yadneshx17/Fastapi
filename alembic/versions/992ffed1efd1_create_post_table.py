"""create post table

Revision ID: 992ffed1efd1
Revises: 
Create Date: 2024-12-14 22:43:15.649972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '992ffed1efd1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass

# undoing 
def downgrade() -> None:
    op.drop_table('posts')
    pass