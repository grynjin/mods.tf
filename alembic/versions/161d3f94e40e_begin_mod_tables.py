"""Begin mod tables.

Revision ID: 161d3f94e40e
Revises: 2092e0fcb096
Create Date: 2014-07-07 23:21:26.398924

"""

# revision identifiers, used by Alembic.
revision = '161d3f94e40e'
down_revision = '2092e0fcb096'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('pretty_name', sa.String(length=256), nullable=True),
    sa.Column('zip_file', sa.String(length=256), nullable=True),
    sa.Column('workshop_id', sa.Integer(), nullable=True),
    sa.Column('package_format', sa.Enum('VPK', 'ZIP', name='package_types'), nullable=True),
    sa.Column('split_class', sa.Boolean(), nullable=True),
    sa.Column('license', sa.String(length=16), nullable=True),
    sa.Column('manifest_steamid', sa.Integer(), nullable=True),
    sa.Column('item_slot', sa.String(length=64), nullable=True),
    sa.Column('image_inventory', sa.String(length=256), nullable=True),
    sa.Column('uploaded', sa.DateTime(), nullable=True),
    sa.Column('visibility', sa.Enum('H', 'Pu', 'Pr', name='visibility_types'), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mod_author',
    sa.Column('mod_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mod_id'], ['mods.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.account_id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mod_author')
    op.drop_table('mods')
    ### end Alembic commands ###
