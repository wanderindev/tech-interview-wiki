"""add excerpt column

Revision ID: 7e36533302d4
Revises: a1fc5a258bde
Create Date: 2024-11-24 23:49:16.893061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e36533302d4'
down_revision = 'a1fc5a258bde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('excerpt', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.drop_column('excerpt')

    # ### end Alembic commands ###
