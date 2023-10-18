"""empty message

Revision ID: 3b86f62212d3
Revises: 4fd7ae799f4c
Create Date: 2023-10-17 21:57:37.373505

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3b86f62212d3'
down_revision = '4fd7ae799f4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('win_lose_draw', postgresql.JSON(astext_type=sa.Text()), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('win_lose_draw')

    # ### end Alembic commands ###
