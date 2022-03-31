from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, inspect, exc
from sqlalchemy.orm import relationship

from sql.database import Base


def get_column_names(model: Base) -> list[str]:
    mapper = inspect(model)
    try:
        columns = mapper.columns
        return [c.name for c in columns]
    except exc.NoInspectionAvailable:
        # TODO: log failure
        return []


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

    occultations = relationship("Occultation", back_populates="entry")
    maneuvers = relationship("Maneuver", back_populates="entry")

    # Fields
    bvec_theta = Column(Float, index=True, nullable=False)
    bvec_mag = Column(Integer, index=True, nullable=False)
    safe = Column(Boolean, doc="Flag indicating whether trajectory avoids unsafe conditions (ring impact, etc)")
    t_entry = Column(Float, index=True, doc="Time of atmospheric entry in days past J2000")
    # entry_trajec = Column(Boolean, nullable=False)

    pos_entry_x = Column(Float, index=True, doc="x component of spacecraft position at time of entry [km]")
    pos_entry_y = Column(Float, index=True, doc="y component of spacecraft position at time of entry [km]")
    pos_entry_z = Column(Float, index=True, doc="z component of spacecraft position at time of entry [km]")
    vel_entry_x = Column(Float, index=True, doc="x component of spacecraft relative entry velocity at time of entry [km]")
    vel_entry_y = Column(Float, index=True, doc="y component of spacecraft relative entry velocity at time of entry [km]")
    vel_entry_z = Column(Float, index=True, doc="z component of spacecraft relative entry velocity at time of entry [km]")

    pos_sun_entry_x = Column(Float, doc="x component of sun position at time of entry [km]")
    pos_sun_entry_y = Column(Float, doc="y component of sun position at time of entry [km]")
    pos_sun_entry_z = Column(Float, doc="z component of sun position at time of entry [km]")
    pos_earth_entry_x = Column(Float, doc="x component of spacecraft position at time of entry [km]")
    pos_earth_entry_y = Column(Float, doc="y component of spacecraft position at time of entry [km]")
    pos_earth_entry_z = Column(Float, doc="z component of spacecraft position at time of entry [km]")
    pos_target_entry_x = Column(Float, doc="x component of target position at time of entry [km]")
    pos_target_entry_y = Column(Float, doc="y component of target position at time of entry [km]")
    pos_target_entry_z = Column(Float, doc="z component of target position at time of entry [km]")

    relay_volume = Column(Float, index=True, nullable=True, doc="Total data volume relayable by entry vehicle.")


class Maneuver(Base):
    # Identity
    __tablename__ = "maneuver"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relationships
    entry_id = Column(Integer, ForeignKey("entry.id"))
    entry = relationship("Entry", back_populates="maneuvers")

    # Fields
    maneuver_type = Column(String, doc="Type of maneuver performed to separate from entry vehicle.")
    dv_maneuver = Column(Float, index=True, doc="Delta V of separation maneuver [km/s].")
    pos_man_x = Column(Float, doc="x component of spacecraft position at time of maneuver [km].")
    pos_man_y = Column(Float, doc="y component of spacecraft position at time of maneuver [km].")
    pos_man_z = Column(Float, doc="z component of spacecraft position at time of maneuver [km].")
    vel_man_x = Column(Float, doc="x component of spacecraft velocity at time of maneuver [km].")
    vel_man_y = Column(Float, doc="y component of spacecraft velocity at time of maneuver [km].")
    vel_man_z = Column(Float, doc="z component of spacecraft velocity at time of maneuver [km].")


class Occultation(Base):
    # Identity
    __tablename__ = "occultation"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relationships
    entry_id = Column(Integer, ForeignKey("entry.id"))
    entry = relationship("Entry", back_populates="occultations")

    # Fields
    t_occ_n = Column(Float, doc="Time that spacecraft enters into occultation relative to the Earth in days past J2000.")
    t_occ_out = Column(Float, doc="Time that spacecraft exits occultation relative to the Earth in days past J2000.")


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

    flybys = relationship("Flyby", back_populates="trajectory")

    # Fields
    t_launch = Column(Float, index=True, doc="time of launch in days past J2000")
    t_arr = Column(Float, index=True, doc="time of target arrival in days past J2000")
    m_arr = Column(Float, index=True, doc="Dry mass deliverable by interplanetary trajectory [kg]")

    v_inf_arr_x = Column(Float, index=True, doc="x component of interplanetary arrival velocity at target [km/s]")
    v_inf_arr_y = Column(Float, index=True, doc="x component of interplanetary arrival velocity at target [km/s]")
    v_inf_arr_z = Column(Float, index=True, doc="x component of interplanetary arrival velocity at target [km/s]")

    c3 = Column(Float, index=True, doc="characteristic energy of launch [km^2/s^2]")
    dv_total = Column(Float, index=True, doc="total DeltaV required for interplanetary trajectory [km/s]")

    pos_sun_arr_x = Column(Float, doc="x component of sun position at time of arrival [km]")
    pos_sun_arr_y = Column(Float, doc="y component of sun position at time of arrival [km]")
    pos_sun_arr_z = Column(Float, doc="z component of sun position at time of arrival [km]")

    pos_sc_arr_x = Column(Float, doc="x component of spacecraft position at time of arrival [km]")
    pos_sc_arr_y = Column(Float, doc="y component of spacecraft position at time of arrival [km]")
    pos_sc_arr_z = Column(Float, doc="z component of spacecraft position at time of arrival [km]")

    pos_target_arr_x = Column(Float, doc="x component of target position at time of arrival [km]")
    pos_target_arr_y = Column(Float, doc="y component of target position at time of arrival [km]")
    pos_target_arr_z = Column(Float, doc="z component of target position at time of arrival [km]")


class Body(Base):
    # Identity
    __tablename__ = "body"
    id = Column(Integer, primary_key=True, doc="corresponds to the ID in the NASA Horizons Database")

    # Relationships
    trajectories = relationship("Trajectory", back_populates="target_body")

    # Fields
    name = Column(String, index=True)
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

    body_id = Column(Integer, ForeignKey("body.id"), index=True)
    flyby_body = relationship("Body")

    # Fields
    order = Column(Integer)
    t_flyby = Column(Float, doc="Time of flyby in days past J2000")
    altitude = Column(Float, doc="Altitude above flyby body surface at flyby hyperbola periapsis [km]")

    v_inf_in_x = Column(Float, doc="x component of incoming flyby v_inifinity [km/s]")
    v_inf_in_y = Column(Float, doc="y component of incoming flyby v_inifinity [km/s]")
    v_inf_in_z = Column(Float, doc="z component of incoming flyby v_inifinity [km/s]")
    v_inf_out_x = Column(Float, doc="x component of incoming flyby v_inifinity [km/s]")
    v_inf_out_y = Column(Float, doc="y component of incoming flyby v_inifinity [km/s]")
    v_inf_out_z = Column(Float, doc="z component of incoming flyby v_inifinity [km/s]")

    # constrain unique(trajectory_id + order)


class Architecture(Base):
    # Identity
    __tablename__ = "architecture"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relationships

    # Fields
    sequence = Column(String, index=True, doc="SQL body IDs of the flybys in order")
