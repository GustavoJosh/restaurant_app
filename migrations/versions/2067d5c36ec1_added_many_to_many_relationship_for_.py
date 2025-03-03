"""Added many-to-many relationship for menu items and branches

Revision ID: 2067d5c36ec1
Revises: d02c240a5ed7
Create Date: 2025-02-25 12:19:09.049113

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2067d5c36ec1'
down_revision = 'd02c240a5ed7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu_items', schema=None) as batch_op:
        batch_op.drop_constraint('menu_items_ibfk_1', type_='foreignkey')
        batch_op.drop_column('branch_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('branch_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('menu_items_ibfk_1', 'branches', ['branch_id'], ['id'])

    # ### end Alembic commands ###
