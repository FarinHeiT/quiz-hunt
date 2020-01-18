"""empty message

Revision ID: 578281619467
Revises: f4f251355904
Create Date: 2020-01-18 09:12:30.556232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '578281619467'
down_revision = 'f4f251355904'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('suggestion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('suggestion')
    # ### end Alembic commands ###