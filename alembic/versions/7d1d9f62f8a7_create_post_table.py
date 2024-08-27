"""create post table

Revision ID: 7d1d9f62f8a7
Revises: 
Create Date: 2024-08-25 19:40:44.331456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d1d9f62f8a7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer()),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id')
        # Add any other columns that are necessary
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
