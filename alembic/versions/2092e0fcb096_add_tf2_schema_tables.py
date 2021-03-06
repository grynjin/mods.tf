"""Add TF2 Schema tables

Revision ID: 2092e0fcb096
Revises: 4db12e0c5745
Create Date: 2014-07-05 23:22:43.523892

"""

# revision identifiers, used by Alembic.
revision = '2092e0fcb096'
down_revision = '4db12e0c5745'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tf2_class',
    sa.Column('class_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('class_name')
    )
    op.create_table('tf2_equip_regions',
    sa.Column('equip_region', sa.String(length=64), nullable=False),
    sa.Column('full_name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('equip_region')
    )
    op.create_table('tf2_schema',
    sa.Column('defindex', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('item_name', sa.String(length=256, collation='utf8_swedish_ci'), nullable=True),
    sa.Column('proper_name', sa.Boolean(), nullable=True),
    sa.Column('item_slot', sa.String(length=64), nullable=True),
    sa.Column('image_url', sa.String(length=256), nullable=True),
    sa.Column('image_url_large', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('defindex')
    )
    op.create_table('tf2_bodygroups',
    sa.Column('bodygroup', sa.String(length=64), nullable=False),
    sa.Column('full_name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('bodygroup')
    )
    op.create_table('tf2_schema_equipregion',
    sa.Column('defindex', sa.Integer(), nullable=True),
    sa.Column('equip_region', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['defindex'], ['tf2_schema.defindex'], ),
    sa.ForeignKeyConstraint(['equip_region'], ['tf2_equip_regions.equip_region'], )
    )
    op.create_table('tf2_schema_bodygroup',
    sa.Column('defindex', sa.Integer(), nullable=True),
    sa.Column('bodygroup', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['bodygroup'], ['tf2_bodygroups.bodygroup'], ),
    sa.ForeignKeyConstraint(['defindex'], ['tf2_schema.defindex'], )
    )
    op.create_table('tf2_schema_classmodel',
    sa.Column('defindex', sa.Integer(), nullable=False),
    sa.Column('class_name', sa.String(length=64), nullable=False),
    sa.Column('model_path', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['class_name'], ['tf2_class.class_name'], ),
    sa.ForeignKeyConstraint(['defindex'], ['tf2_schema.defindex'], ),
    sa.PrimaryKeyConstraint('defindex', 'class_name')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tf2_schema_classmodel')
    op.drop_table('tf2_schema_bodygroup')
    op.drop_table('tf2_schema_equipregion')
    op.drop_table('tf2_bodygroups')
    op.drop_table('tf2_schema')
    op.drop_table('tf2_equip_regions')
    op.drop_table('tf2_class')
    ### end Alembic commands ###
