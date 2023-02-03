"""add content column to posts table

Revision ID: 038e01847ef7
Revises: 9ede27084441
Create Date: 2023-02-02 11:07:07.241434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '038e01847ef7'
down_revision = '9ede27084441'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
