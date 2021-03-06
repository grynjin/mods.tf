"""Add mod image table.

Revision ID: 28beb21ba379
Revises: 30f34c437dbc
Create Date: 2014-07-27 22:11:13.736429

"""

# revision identifiers, used by Alembic.
revision = '28beb21ba379'
down_revision = '30f34c437dbc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mod_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=256), nullable=False),
    sa.Column('mod_id', sa.Integer(), nullable=False),
    sa.Column('uploaded', sa.DateTime(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mod_id'], ['mods.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mod_image')
    ### end Alembic commands ###
