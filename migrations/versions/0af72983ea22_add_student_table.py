"""Add Student Table

Revision ID: 0af72983ea22
Revises: 
Create Date: 2022-05-02 22:31:19.501946

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0af72983ea22'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('students',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('first_name', sa.String(length=128), nullable=False),
                    sa.Column('last_name', sa.String(length=128), nullable=False),
                    sa.Column('email', sa.String(length=128), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table('students')
