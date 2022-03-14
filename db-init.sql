CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> db3508e20429

CREATE TABLE architectures (
    id INTEGER NOT NULL, 
    sequence VARCHAR, 
    PRIMARY KEY (id)
);

CREATE TABLE bodies (
    id INTEGER NOT NULL, 
    horizons_id INTEGER, 
    name VARCHAR, 
    PRIMARY KEY (id)
);

CREATE TABLE entries (
    id INTEGER NOT NULL, 
    bvec_theta FLOAT NOT NULL, 
    bvec_abs INTEGER NOT NULL, 
    entry_trajec BOOLEAN NOT NULL, 
    state_eq_rx FLOAT, 
    state_eq_ry FLOAT, 
    state_eq_rz FLOAT, 
    state_eq_vx FLOAT, 
    state_eq_vy FLOAT, 
    state_eq_vz FLOAT, 
    safe BOOLEAN NOT NULL, 
    entry_state_rx FLOAT NOT NULL, 
    entry_state_ry FLOAT NOT NULL, 
    entry_state_rz FLOAT NOT NULL, 
    entry_state_vx FLOAT NOT NULL, 
    entry_state_vy FLOAT NOT NULL, 
    entry_state_vz FLOAT NOT NULL, 
    lon_entry FLOAT, 
    lat_entry FLOAT, 
    v_rot_x FLOAT, 
    v_rot_y FLOAT, 
    v_rot_z FLOAT, 
    fpa FLOAT, 
    v_rel_entry_x FLOAT, 
    v_rel_entry_y FLOAT, 
    v_rel_entry_z FLOAT, 
    PRIMARY KEY (id)
);

CREATE TABLE flybys (
    id INTEGER NOT NULL, 
    days INTEGER, 
    "order" INTEGER, 
    PRIMARY KEY (id)
);

CREATE TABLE trajectories (
    id INTEGER NOT NULL, 
    launch_days FLOAT, 
    arrive_days FLOAT, 
    v_inf_x FLOAT, 
    v_inf_y FLOAT, 
    v_inf_z FLOAT, 
    planet_pos_x FLOAT, 
    planet_pos_y FLOAT, 
    planet_pos_z FLOAT, 
    planet_vel_x FLOAT, 
    planet_vel_y FLOAT, 
    planet_vel_z FLOAT, 
    c3 FLOAT, 
    delta_v FLOAT, 
    arrival_mass FLOAT, 
    PRIMARY KEY (id)
);

INSERT INTO alembic_version (version_num) VALUES ('db3508e20429');

