"""Generate schema

Revision ID: 2e9686bf76a3
Revises: 
Create Date: 2022-04-05 16:55:48.838177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2e9686bf76a3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "architecture",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sequence", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("architecture", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_architecture_sequence"), ["sequence"], unique=False)

    op.create_table(
        "body",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("radius", sa.Float(), nullable=True),
        sa.Column("mu", sa.Float(), nullable=True),
        sa.Column("period", sa.Float(), nullable=True),
        sa.Column("pole_vec_x", sa.Float(), nullable=True),
        sa.Column("pole_vec_y", sa.Float(), nullable=True),
        sa.Column("pole_vec_z", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("body", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_body_name"), ["name"], unique=False)

    op.create_table(
        "trajectory",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("body_id", sa.Integer(), nullable=True),
        sa.Column("architecture_id", sa.Integer(), nullable=True),
        sa.Column("t_launch", sa.Float(), nullable=True),
        sa.Column("t_arr", sa.Float(), nullable=True),
        sa.Column("v_inf_arr_x", sa.Float(), nullable=True),
        sa.Column("v_inf_arr_y", sa.Float(), nullable=True),
        sa.Column("v_inf_arr_z", sa.Float(), nullable=True),
        sa.Column("c3", sa.Float(), nullable=True),
        sa.Column("dv_total", sa.Float(), nullable=True),
        sa.Column("pos_sun_arr_x", sa.Float(), nullable=True),
        sa.Column("pos_sun_arr_y", sa.Float(), nullable=True),
        sa.Column("pos_sun_arr_z", sa.Float(), nullable=True),
        sa.Column("pos_sc_arr_x", sa.Float(), nullable=True),
        sa.Column("pos_sc_arr_y", sa.Float(), nullable=True),
        sa.Column("pos_sc_arr_z", sa.Float(), nullable=True),
        sa.Column("pos_target_arr_x", sa.Float(), nullable=True),
        sa.Column("pos_target_arr_y", sa.Float(), nullable=True),
        sa.Column("pos_target_arr_z", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["architecture_id"],
            ["architecture.id"],
        ),
        sa.ForeignKeyConstraint(
            ["body_id"],
            ["body.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("trajectory", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_trajectory_c3"), ["c3"], unique=False)
        batch_op.create_index(batch_op.f("ix_trajectory_dv_total"), ["dv_total"], unique=False)
        batch_op.create_index(batch_op.f("ix_trajectory_t_arr"), ["t_arr"], unique=False)
        batch_op.create_index(batch_op.f("ix_trajectory_t_launch"), ["t_launch"], unique=False)
        batch_op.create_index(
            batch_op.f("ix_trajectory_v_inf_arr_x"), ["v_inf_arr_x"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_trajectory_v_inf_arr_y"), ["v_inf_arr_y"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_trajectory_v_inf_arr_z"), ["v_inf_arr_z"], unique=False
        )

    op.create_table(
        "entry",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("body_id", sa.Integer(), nullable=True),
        sa.Column("trajectory_id", sa.Integer(), nullable=True),
        sa.Column("bvec_theta", sa.Float(), nullable=False),
        sa.Column("bvec_mag", sa.Integer(), nullable=False),
        sa.Column("safe", sa.Boolean(), nullable=True),
        sa.Column("t_entry", sa.Float(), nullable=True),
        sa.Column("pos_entry_x", sa.Float(), nullable=True),
        sa.Column("pos_entry_y", sa.Float(), nullable=True),
        sa.Column("pos_entry_z", sa.Float(), nullable=True),
        sa.Column("vel_entry_x", sa.Float(), nullable=True),
        sa.Column("vel_entry_y", sa.Float(), nullable=True),
        sa.Column("vel_entry_z", sa.Float(), nullable=True),
        sa.Column("pos_sun_entry_x", sa.Float(), nullable=True),
        sa.Column("pos_sun_entry_y", sa.Float(), nullable=True),
        sa.Column("pos_sun_entry_z", sa.Float(), nullable=True),
        sa.Column("pos_earth_entry_x", sa.Float(), nullable=True),
        sa.Column("pos_earth_entry_y", sa.Float(), nullable=True),
        sa.Column("pos_earth_entry_z", sa.Float(), nullable=True),
        sa.Column("pos_target_entry_x", sa.Float(), nullable=True),
        sa.Column("pos_target_entry_y", sa.Float(), nullable=True),
        sa.Column("pos_target_entry_z", sa.Float(), nullable=True),
        sa.Column("relay_volume", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["body_id"],
            ["body.id"],
        ),
        sa.ForeignKeyConstraint(
            ["trajectory_id"],
            ["trajectory.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("entry", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_entry_bvec_mag"), ["bvec_mag"], unique=False)
        batch_op.create_index(batch_op.f("ix_entry_bvec_theta"), ["bvec_theta"], unique=False)
        batch_op.create_index(batch_op.f("ix_entry_pos_entry_x"), ["pos_entry_x"], unique=False)
        batch_op.create_index(batch_op.f("ix_entry_pos_entry_y"), ["pos_entry_y"], unique=False)
        batch_op.create_index(batch_op.f("ix_entry_pos_entry_z"), ["pos_entry_z"], unique=False)
        batch_op.create_index(batch_op.f("ix_entry_relay_volume"), ["relay_volume"], unique=False)
        batch_op.create_index(batch_op.f("ix_entry_t_entry"), ["t_entry"], unique=False)
        batch_op.create_index(batch_op.f("ix_entry_vel_entry_x"), ["vel_entry_x"], unique=False)
        batch_op.create_index(batch_op.f("ix_entry_vel_entry_y"), ["vel_entry_y"], unique=False)
        batch_op.create_index(batch_op.f("ix_entry_vel_entry_z"), ["vel_entry_z"], unique=False)

    op.create_table(
        "flyby",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("trajectory_id", sa.Integer(), nullable=True),
        sa.Column("body_id", sa.Integer(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=True),
        sa.Column("t_flyby", sa.Float(), nullable=True),
        sa.Column("altitude", sa.Float(), nullable=True),
        sa.Column("v_inf_in_x", sa.Float(), nullable=True),
        sa.Column("v_inf_in_y", sa.Float(), nullable=True),
        sa.Column("v_inf_in_z", sa.Float(), nullable=True),
        sa.Column("v_inf_out_x", sa.Float(), nullable=True),
        sa.Column("v_inf_out_y", sa.Float(), nullable=True),
        sa.Column("v_inf_out_z", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["body_id"],
            ["body.id"],
        ),
        sa.ForeignKeyConstraint(
            ["trajectory_id"],
            ["trajectory.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("flyby", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_flyby_body_id"), ["body_id"], unique=False)

    op.create_table(
        "occultation",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("trajectory_id", sa.Integer(), nullable=True),
        sa.Column("t_occ_n", sa.Float(), nullable=True),
        sa.Column("t_occ_out", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["trajectory_id"],
            ["trajectory.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "maneuver",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("entry_id", sa.Integer(), nullable=True),
        sa.Column("maneuver_type", sa.String(), nullable=True),
        sa.Column("dv_maneuver", sa.Float(), nullable=True),
        sa.Column("pos_man_x", sa.Float(), nullable=True),
        sa.Column("pos_man_y", sa.Float(), nullable=True),
        sa.Column("pos_man_z", sa.Float(), nullable=True),
        sa.Column("vel_man_x", sa.Float(), nullable=True),
        sa.Column("vel_man_y", sa.Float(), nullable=True),
        sa.Column("vel_man_z", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["entry_id"],
            ["entry.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("maneuver", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_maneuver_dv_maneuver"), ["dv_maneuver"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("maneuver", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_maneuver_dv_maneuver"))

    op.drop_table("maneuver")
    op.drop_table("occultation")
    with op.batch_alter_table("flyby", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_flyby_body_id"))

    op.drop_table("flyby")
    with op.batch_alter_table("entry", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_entry_vel_entry_z"))
        batch_op.drop_index(batch_op.f("ix_entry_vel_entry_y"))
        batch_op.drop_index(batch_op.f("ix_entry_vel_entry_x"))
        batch_op.drop_index(batch_op.f("ix_entry_t_entry"))
        batch_op.drop_index(batch_op.f("ix_entry_relay_volume"))
        batch_op.drop_index(batch_op.f("ix_entry_pos_entry_z"))
        batch_op.drop_index(batch_op.f("ix_entry_pos_entry_y"))
        batch_op.drop_index(batch_op.f("ix_entry_pos_entry_x"))
        batch_op.drop_index(batch_op.f("ix_entry_bvec_theta"))
        batch_op.drop_index(batch_op.f("ix_entry_bvec_mag"))

    op.drop_table("entry")
    with op.batch_alter_table("trajectory", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_trajectory_v_inf_arr_z"))
        batch_op.drop_index(batch_op.f("ix_trajectory_v_inf_arr_y"))
        batch_op.drop_index(batch_op.f("ix_trajectory_v_inf_arr_x"))
        batch_op.drop_index(batch_op.f("ix_trajectory_t_launch"))
        batch_op.drop_index(batch_op.f("ix_trajectory_t_arr"))
        batch_op.drop_index(batch_op.f("ix_trajectory_dv_total"))
        batch_op.drop_index(batch_op.f("ix_trajectory_c3"))

    op.drop_table("trajectory")
    with op.batch_alter_table("body", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_body_name"))

    op.drop_table("body")
    with op.batch_alter_table("architecture", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_architecture_sequence"))

    op.drop_table("architecture")
    # ### end Alembic commands ###
