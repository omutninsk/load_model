"""empty message

Revision ID: 432de5c726d3
Revises: 
Create Date: 2023-04-22 17:05:00.448809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '432de5c726d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('action', sa.String(length=20), nullable=True),
    sa.Column('value', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('action'),
    sa.UniqueConstraint('value')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logs')
    # ### end Alembic commands ###