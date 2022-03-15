from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Entry(Base):
    # Identity
    __tablename__ = "entry"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relationships
    # NOTE: Technically, Entry is linked to Body via the intermediate Trajectory relationship
    #       so this direct link is not needed but could still be helpful to include for clarity?
    body_id = Column(Integer, ForeignKey("body.id"))
    target_body = relationship("Body")

    trajectory_id = Column(Integer, ForeignKey("trajectory.id"))
    trajectory = relationship("Trajectory", back_populates="entries")

    # Fields
    bvec_theta = Column(Float, nullable=False)
    bvec_abs = Column(Integer, nullable=False)
    entry_trajec = Column(Boolean, nullable=False)

    state_eq_rx = Column(Float)
    state_eq_ry = Column(Float)
    state_eq_rz = Column(Float)
    state_eq_vx = Column(Float)
    state_eq_vy = Column(Float)
    state_eq_vz = Column(Float)

    safe = Column(Boolean, nullable=False)
    entry_state_rx = Column(Float, nullable=False)
    entry_state_ry = Column(Float, nullable=False)
    entry_state_rz = Column(Float, nullable=False)
    entry_state_vx = Column(Float, nullable=False)
    entry_state_vy = Column(Float, nullable=False)
    entry_state_vz = Column(Float, nullable=False)

    lon_entry = Column(Float)
    lat_entry = Column(Float)

    v_rot_x = Column(Float)
    v_rot_y = Column(Float)
    v_rot_z = Column(Float)

    fpa = Column(Float)

    v_rel_entry_x = Column(Float)
    v_rel_entry_y = Column(Float)
    v_rel_entry_z = Column(Float)


class Trajectory(Base):
    # Identity
    __tablename__ = "trajectory"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relationships
    body_id = Column(Integer, ForeignKey("body.id"))
    target_body = relationship("Body", back_populates="trajectories")

    architecture_id = Column(Integer, ForeignKey("architecture.id"))
    architecture = relationship("Architecture")

    entries = relationship("Entry", back_populates="trajectory")

    # Fields
    t_launch = Column(Float, index=True, doc="time of launch in days past J2000")
    t_arr = Column(Float, index=True, doc="time of target arrival in days past J2000")

    v_inf_arr_x = Column(Float, index=True, doc="x component of interplanetary arrival velocity at target [km/s]")
    v_inf_arr_y = Column(Float, index=True, doc="x component of interplanetary arrival velocity at target [km/s]")
    v_inf_arr_z = Column(Float, index=True, doc="x component of interplanetary arrival velocity at target [km/s]")

    pos_sun_x = Column(Float, doc="x component of sun position at time of arrival [km]")
    pos_sun_y = Column(Float, doc="y component of sun position at time of arrival [km]")
    pos_sun_z = Column(Float, doc="z component of sun position at time of arrival [km]")

    pos_earth_x = Column(Float, doc="x component of earth position at time of arrival [km]")
    pos_earth_y = Column(Float, doc="y component of earth position at time of arrival [km]")
    pos_earth_z = Column(Float, doc="z component of earth position at time of arrival [km]")

    pos_target_x = Column(Float, doc="x component of target position at time of arrival [km]")
    pos_target_y = Column(Float, doc="y component of target position at time of arrival [km]")
    pos_target_z = Column(Float, doc="z component of target position at time of arrival [km]")

    pos_sc_x = Column(Float, doc="x component of spacecraft position at time of arrival [km]")
    pos_sc_y = Column(Float, doc="y component of spacecraft position at time of arrival [km]")
    pos_sc_z = Column(Float, doc="z component of spacecraft position at time of arrival [km]")

    c3 = Column(Float, index=True, doc="characteristic energy of launch [km^2/s^2]")
    dv_total = Column(Float, index=True, doc="total DeltaV required for interplanetary trajectory [km/s]")
    arrival_mass = Column(Float)  # TODO: Is this being removed?


class Body(Base):
    # Identity
    __tablename__ = "body"
    id = Column(Integer, primary_key=True, doc="corresponds to the ID in the NASA Horizons Database")

    # Relationships
    trajectories = relationship("Trajectory", back_populates="target_body")

    # Fields
    name = Column(String)
    radius = Column(Float, doc="mean radius of body (km)")
    mu = Column(Float, doc="gravity parameter [km^3/s^2]")
    period = Column(Float, doc="body rotational period [days]")
    pole_vec_x = Column(Float, doc="x component of body spin pole unit vector represented in EMO2000 frame")
    pole_vec_y = Column(Float, doc="y component of body spin pole unit vector represented in EMO2000 frame")
    pole_vec_z = Column(Float, doc="z component of body spin pole unit vector represented in EMO2000 frame")


class Flyby(Base):
    # Identity
    __tablename__ = "flyby"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relationships
    trajectory_id = Column(Integer, ForeignKey("trajectory.id"))
    trajectory = relationship("Trajectory", back_populates="flybys")

    body_id = Column(Integer, ForeignKey("body.id"))
    flyby_body = relationship("Body")

    # Fields
    days = Column(Float)
    order = Column(Integer)

    # constrain unique(trajectory_id + order)


class Architecture(Base):
    # Identity
    __tablename__ = "architecture"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relationships

    # Fields
    sequence = Column(String)
