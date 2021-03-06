"""Add image_url column to user.py

Revision ID: 06fd73265325
Revises: 3ef9611cc9ae
Create Date: 2020-12-06 19:49:11.613462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06fd73265325'
down_revision = '3ef9611cc9ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.String(length=2048), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('image_url')

    # ### end Alembic commands ###
