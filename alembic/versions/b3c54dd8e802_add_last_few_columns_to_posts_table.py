"""add last few columns to posts table

Revision ID: b3c54dd8e802
Revises: 1f0f2b7d3f3e
Create Date: 2023-02-02 12:15:04.301782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3c54dd8e802'
down_revision = '1f0f2b7d3f3e'
branch_labels = None
depends_on = None


def upgrade():
    op. add_column('posts', sa. Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),) 
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP (timezone=True), nullable=False, server_default=sa. text
        ('NOW()')),)
    pass


def downgrade():
    op.drop_column ('posts','published')
    op.drop_column('posts','created_at')
    pass
