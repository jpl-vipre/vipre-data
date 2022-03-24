CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE architecture (
	id INTEGER NOT NULL, 
	sequence VARCHAR, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_architecture_sequence ON architecture (sequence);
CREATE TABLE body (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	radius FLOAT, 
	mu FLOAT, 
	period FLOAT, 
	pole_vec_x FLOAT, 
	pole_vec_y FLOAT, 
	pole_vec_z FLOAT, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_body_name ON body (name);
CREATE TABLE trajectory (
	id INTEGER NOT NULL, 
	body_id INTEGER, 
	architecture_id INTEGER, 
	t_launch FLOAT, 
	t_arr FLOAT, 
	v_inf_arr_x FLOAT, 
	v_inf_arr_y FLOAT, 
	v_inf_arr_z FLOAT, 
	pos_sun_x FLOAT, 
	pos_sun_y FLOAT, 
	pos_sun_z FLOAT, 
	pos_earth_x FLOAT, 
	pos_earth_y FLOAT, 
	pos_earth_z FLOAT, 
	pos_target_x FLOAT, 
	pos_target_y FLOAT, 
	pos_target_z FLOAT, 
	pos_sc_x FLOAT, 
	pos_sc_y FLOAT, 
	pos_sc_z FLOAT, 
	c3 FLOAT, 
	dv_total FLOAT, 
	arrival_mass FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(architecture_id) REFERENCES architecture (id), 
	FOREIGN KEY(body_id) REFERENCES body (id)
);
CREATE INDEX ix_trajectory_arrival_mass ON trajectory (arrival_mass);
CREATE INDEX ix_trajectory_c3 ON trajectory (c3);
CREATE INDEX ix_trajectory_dv_total ON trajectory (dv_total);
CREATE INDEX ix_trajectory_t_arr ON trajectory (t_arr);
CREATE INDEX ix_trajectory_t_launch ON trajectory (t_launch);
CREATE INDEX ix_trajectory_v_inf_arr_x ON trajectory (v_inf_arr_x);
CREATE INDEX ix_trajectory_v_inf_arr_y ON trajectory (v_inf_arr_y);
CREATE INDEX ix_trajectory_v_inf_arr_z ON trajectory (v_inf_arr_z);
CREATE TABLE flyby (
	id INTEGER NOT NULL, 
	trajectory_id INTEGER, 
	body_id INTEGER, 
	altitude FLOAT, 
	days FLOAT, 
	"order" INTEGER, 
	v_inf_in_x FLOAT, 
	v_inf_in_y FLOAT, 
	v_inf_in_z FLOAT, 
	v_inf_out_x FLOAT, 
	v_inf_out_y FLOAT, 
	v_inf_out_z FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(body_id) REFERENCES body (id), 
	FOREIGN KEY(trajectory_id) REFERENCES trajectory (id)
);
CREATE INDEX ix_flyby_body_id ON flyby (body_id);
CREATE TABLE occultation (
	id INTEGER NOT NULL, 
	entry_id INTEGER, 
	t_occ_n FLOAT, 
	t_occ_out FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(entry_id) REFERENCES entry (id)
);
CREATE TABLE maneuver (
	id INTEGER NOT NULL, 
	entry_id INTEGER, 
	maneuver_type VARCHAR, 
	dv_maneuver FLOAT, 
	pos_man_x FLOAT, 
	pos_man_y FLOAT, 
	pos_man_z FLOAT, 
	vel_man_x FLOAT, 
	vel_man_y FLOAT, 
	vel_man_z FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(entry_id) REFERENCES entry (id)
);
CREATE INDEX ix_maneuver_dv_maneuver ON maneuver (dv_maneuver);
CREATE TABLE IF NOT EXISTS "entry" (
	id INTEGER NOT NULL, 
	body_id INTEGER, 
	trajectory_id INTEGER, 
	bvec_theta FLOAT NOT NULL, 
	bvec_mag INTEGER NOT NULL, 
	safe BOOLEAN, 
	t_entry FLOAT, 
	pos_entry_x FLOAT, 
	pos_entry_y FLOAT, 
	pos_entry_z FLOAT, 
	vel_entry_x FLOAT, 
	vel_entry_y FLOAT, 
	vel_entry_z FLOAT, 
	pos_sun_entry_x FLOAT, 
	pos_sun_entry_y FLOAT, 
	pos_sun_entry_z FLOAT, 
	pos_sc_entry_x FLOAT, 
	pos_sc_entry_y FLOAT, 
	pos_sc_entry_z FLOAT, 
	pos_target_entry_x FLOAT, 
	pos_target_entry_y FLOAT, 
	pos_target_entry_z FLOAT, 
	relay_volume FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(trajectory_id) REFERENCES trajectory (id), 
	FOREIGN KEY(body_id) REFERENCES body (id)
);
CREATE INDEX ix_entry_pos_entry_y ON entry (pos_entry_y);
CREATE INDEX ix_entry_t_entry ON entry (t_entry);
CREATE INDEX ix_entry_pos_entry_x ON entry (pos_entry_x);
CREATE INDEX ix_entry_pos_entry_z ON entry (pos_entry_z);
CREATE INDEX ix_entry_bvec_theta ON entry (bvec_theta);
CREATE INDEX ix_entry_relay_volume ON entry (relay_volume);
CREATE INDEX ix_entry_bvec_mag ON entry (bvec_mag);
CREATE INDEX ix_entry_vel_entry_y ON entry (vel_entry_y);
CREATE INDEX ix_entry_vel_entry_z ON entry (vel_entry_z);
CREATE INDEX ix_entry_vel_entry_x ON entry (vel_entry_x);
