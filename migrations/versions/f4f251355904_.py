"""empty message

Revision ID: f4f251355904
Revises: feed6fbcbb54
Create Date: 2020-01-15 20:32:16.261358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4f251355904'
down_revision = 'feed6fbcbb54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('poll', sa.Column('image_name', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('poll', 'image_name')
    # ### end Alembic commands ###
