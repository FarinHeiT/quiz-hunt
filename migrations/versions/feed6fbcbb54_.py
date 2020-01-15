"""empty message

Revision ID: feed6fbcbb54
Revises: 
Create Date: 2020-01-15 12:00:49.926361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'feed6fbcbb54'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('poll', sa.Column('description', sa.Text(length=400), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('poll', 'description')
    # ### end Alembic commands ###
