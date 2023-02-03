"""create posts table

Revision ID: 9ede27084441
Revises: 
Create Date: 2023-02-01 14:57:12.923209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ede27084441'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))
    pass

def downgrade():
    op.drop_table('posts')
    pass
