"""create foriegn-key posts

Revision ID: bfe0fdb84959
Revises: c0380ece329e
Create Date: 2024-08-25 19:43:36.865436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bfe0fdb84959'
down_revision: Union[str, None] = 'c0380ece329e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass