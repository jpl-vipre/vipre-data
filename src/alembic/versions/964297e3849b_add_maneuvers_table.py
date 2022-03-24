"""Add maneuvers table

Revision ID: 964297e3849b
Revises: 7bbbb4dc8221
Create Date: 2022-03-24 13:32:51.548641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '964297e3849b'
down_revision = '7bbbb4dc8221'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'maneuver',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('entry_id', sa.Integer(), nullable=True),
        sa.Column('maneuver_type', sa.String(), nullable=True),
        sa.Column('dv_maneuver', sa.Float(), nullable=True),
        sa.Column('pos_man_x', sa.Float(), nullable=True),
        sa.Column('pos_man_y', sa.Float(), nullable=True),
        sa.Column('pos_man_z', sa.Float(), nullable=True),
        sa.Column('vel_man_x', sa.Float(), nullable=True),
        sa.Column('vel_man_y', sa.Float(), nullable=True),
        sa.Column('vel_man_z', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['entry_id'], ['entry.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_maneuver_dv_maneuver'), 'maneuver', ['dv_maneuver'], unique=False)
    op.drop_index('ix_entry_dv_maneuver', table_name='entry')
    op.drop_column('entry', 'pos_man_y')
    op.drop_column('entry', 'dv_maneuver')
    op.drop_column('entry', 'vel_man_z')
    op.drop_column('entry', 'maneuver')
    op.drop_column('entry', 'pos_man_z')
    op.drop_column('entry', 'vel_man_y')
    op.drop_column('entry', 'pos_man_x')
    op.drop_column('entry', 'vel_man_x')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entry', sa.Column('vel_man_x', sa.FLOAT(), nullable=True))
    op.add_column('entry', sa.Column('pos_man_x', sa.FLOAT(), nullable=True))
    op.add_column('entry', sa.Column('vel_man_y', sa.FLOAT(), nullable=True))
    op.add_column('entry', sa.Column('pos_man_z', sa.FLOAT(), nullable=True))
    op.add_column('entry', sa.Column('maneuver', sa.VARCHAR(), nullable=True))
    op.add_column('entry', sa.Column('vel_man_z', sa.FLOAT(), nullable=True))
    op.add_column('entry', sa.Column('dv_maneuver', sa.FLOAT(), nullable=True))
    op.add_column('entry', sa.Column('pos_man_y', sa.FLOAT(), nullable=True))
    op.create_index('ix_entry_dv_maneuver', 'entry', ['dv_maneuver'], unique=False)
    op.drop_index(op.f('ix_maneuver_dv_maneuver'), table_name='maneuver')
    op.drop_table('maneuver')
    # ### end Alembic commands ###
