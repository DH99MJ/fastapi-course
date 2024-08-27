"""create a some column for posts table

Revision ID: 5de7e8247f6f
Revises: bfe0fdb84959
Create Date: 2024-08-25 19:47:52.046214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision: str = '5de7e8247f6f'
down_revision: Union[str, None] = 'bfe0fdb84959'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Get the current connection
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)

    # Check if the 'published' column already exists
    columns = [column['name'] for column in inspector.get_columns('posts')]
    if 'published' not in columns:
        op.add_column('posts',
                      sa.Column('published', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')))
    if 'created_at' not in columns:
        op.add_column('posts',
                      sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))

def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
