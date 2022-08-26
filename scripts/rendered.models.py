from typing import Type

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text, Float, inspect, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

VERSION = "0.3.1"

Base = declarative_base()


def get_column_names(model: Type[Base]) -> list[str]:
    mapper = inspect(model)
    try:
        columns = mapper.columns
        return [c.name for c in columns]
    except exc.NoInspectionAvailable:
        # TODO: log failure
        return []


class Architecture(Base):
    # Identity
    __tablename__ = "architecture"

    # Relationships

    # Fields
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    sequence = Column(Text, index=True, doc="SQL body IDs of the flybys in order")


class Body(Base):
    # Identity
    __tablename__ = "body"

    # Relationships
    trajectories = relationship("Trajectory", back_populates="target_body")

    # Fields
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
        doc="corresponds to the ID in the NASA Horizons Database",
    )
    name = Column(Text, index=True, doc="name of body")
    radius = Column(Float, doc="mean radius of body [km]")
    mu = Column(Float, doc="gravity parameter [km^3/s^2]")
    period = Column(Float, doc="body rotational period [days]")
    pole_vec_x = Column(
        Float, doc="x component of body spin pole unit vector represented in EMO2000 frame"
    )
    pole_vec_y = Column(
        Float, doc="y component of body spin pole unit vector represented in EMO2000 frame"
    )
    pole_vec_z = Column(
        Float, doc="z component of body spin pole unit vector represented in EMO2000 frame"
    )


class Datarate(Base):
    # Identity
    __tablename__ = "datarate"

    # Relationships
    entry = relationship("Entry", back_populates="datarates")

    # Fields
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    entry_id = Column(
        Integer, ForeignKey("entry.id"), index=True, doc="ID of the parent Entry row in database"
    )
    order = Column(Integer, index=True, doc="Order of this tuple in the datarate time series")
    time = Column(
        Integer,
        nullable=True,
        doc="Downsampled time in datarate time series. Time is seconds after entry",
    )
    rate = Column(Float, nullable=True, doc="Downsampled datarate in datarate time series")


class Entry(Base):
    # Identity
    __tablename__ = "entry"

    # Relationships
    target_body = relationship("Body")
    trajectory = relationship("Trajectory", back_populates="entries")
    datarates = relationship("Datarate", back_populates="entry")
    maneuvers = relationship("Maneuver", back_populates="entry")

    # Fields
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    body_id = Column(
        Integer, ForeignKey("body.id"), index=True, doc="ID of the parent Body in the database"
    )
    trajectory_id = Column(
        Integer,
        ForeignKey("trajectory.id"),
        index=True,
        doc="ID of the parent Trajectory in the database",
    )
    bvec_theta = Column(Float, index=True, doc="Angle on B-plane for target arrival [rad]")
    bvec_mag = Column(
        Float, index=True, doc="Radial distance from body origin for target arrival [km]"
    )
    safe = Column(
        Boolean,
        doc="Flag indicating whether trajectory avoids unsafe conditions (ring impact, etc)",
    )
    t_entry = Column(Integer, index=True, doc="Time of atmospheric entry in seconds past J2000")
    pos_entry_x = Column(Float, doc="x component of spacecraft position at time of entry [km]")
    pos_entry_y = Column(Float, doc="y component of spacecraft position at time of entry [km]")
    pos_entry_z = Column(Float, doc="z component of spacecraft position at time of entry [km]")
    pos_entry_mag = Column(
        Float, index=True, doc="magnitude of spacecraft position at time of entry"
    )
    pos_entry_lat = Column(
        Float, index=True, doc="latitude of spacecraft position at time of entry"
    )
    pos_entry_lon = Column(
        Float, index=True, doc="longitude of spacecraft position at time of entry"
    )
    vel_entry_x = Column(
        Float, doc="X component of spacecraft relative entry velocity at time of entry [km/s]"
    )
    vel_entry_y = Column(
        Float, doc="y component of spacecraft relative entry velocity at time of entry [km/s]"
    )
    vel_entry_z = Column(
        Float, doc="z component of spacecraft relative entry velocity at time of entry [km/s]"
    )
    vel_entry_mag = Column(
        Float,
        index=True,
        doc="magnitude of spacecraft relative entry velocity at time of entry [km/s]",
    )
    flight_path_angle = Column(
        Float, index=True, nullable=True, doc="flight path angle at point of entry"
    )
    solar_phase_angle = Column(Float, index=True, nullable=True, doc="Sun-Target-Vinfinity Angle")
    solar_conj_angle = Column(Float, index=True, nullable=True, doc="Sun-Target-Earth Angle")
    solar_incidence_angle = Column(
        Float, index=True, nullable=True, doc="Sun-Target-Entry Position Angle"
    )
    pos_sun_entry_x = Column(Float, doc="x component of sun position at time of entry [km]")
    pos_sun_entry_y = Column(Float, doc="y component of sun position at time of entry [km]")
    pos_sun_entry_z = Column(Float, doc="z component of sun position at time of entry [km]")
    pos_earth_entry_x = Column(Float, doc="x component of Earth position at time of entry [km]")
    pos_earth_entry_y = Column(Float, doc="y component of Earth position at time of entry [km]")
    pos_earth_entry_z = Column(Float, doc="z component of Earth position at time of entry [km]")
    pos_target_entry_x = Column(Float, doc="x component of target position at time of entry [km]")
    pos_target_entry_y = Column(Float, doc="y component of target position at time of entry [km]")
    pos_target_entry_z = Column(Float, doc="z component of target position at time of entry [km]")
    rot_vel_entry_x = Column(
        Float,
        doc="X component of spacecraft relative entry velocity at time of entry in planet rotating frame [km/s]",
    )
    rot_vel_entry_y = Column(
        Float,
        doc="y component of spacecraft relative entry velocity at time of entry in planet rotating frame [km/s]",
    )
    rot_vel_entry_z = Column(
        Float,
        doc="z component of spacecraft relative entry velocity at time of entry in planet rotating frame [km/s]",
    )
    rot_vel_entry_mag = Column(
        Float,
        index=True,
        doc="magnitude of spacecraft relative entry velocity at time of entry in planet rotating frame [km/s]",
    )
    relay_volume = Column(
        Float, index=True, nullable=True, doc="Total data volume relayable by entry vehicle."
    )
    ring_shadow = Column(
        Boolean, nullable=True, doc="true if the entry is in the shadow of a planet's ring"
    )
    carrier_orbit = Column(
        Text,
        nullable=True,
        doc="label describing the pre-divert orbit. Primarily used to distinguish between flyby and orbitting probe releases.",
    )


class Flyby(Base):
    # Identity
    __tablename__ = "flyby"

    # Relationships
    trajectory = relationship("Trajectory", back_populates="flybys")
    flyby_body = relationship("Body")

    # Fields
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    trajectory_id = Column(
        Integer, ForeignKey("trajectory.id"), index=True, doc="SQL trajectory ID"
    )
    body_id = Column(Integer, ForeignKey("body.id"), index=True, doc="SQL body ID of flyby body")
    order = Column(Integer, doc="Order of this flyby in trajectory's flyby sequence")
    t_flyby = Column(Integer, doc="Time of flyby in seconds past J2000")
    altitude = Column(
        Float, doc="Altitude above flyby body surface at flyby hyperbola periapsis [km]"
    )
    v_inf_in_x = Column(Float, doc="x component of incoming flyby v_infinity [km/s]")
    v_inf_in_y = Column(Float, doc="y component of incoming flyby v_infinity [km/s]")
    v_inf_in_z = Column(Float, doc="z component of incoming flyby v_infinity [km/s]")
    v_inf_in_mag = Column(Float, doc="magnitude component of incoming flyby v_infinity [km/s]")
    v_inf_out_x = Column(Float, doc="x component of outgoing flyby v_infinity [km/s]")
    v_inf_out_y = Column(Float, doc="y component of outgoing flyby v_infinity [km/s]")
    v_inf_out_z = Column(Float, doc="z component of outgoing flyby v_infinity [km/s]")
    v_inf_out_mag = Column(Float, doc="magnitude of outgoing flyby v_infinity [km/s]")


class Maneuver(Base):
    # Identity
    __tablename__ = "maneuver"

    # Relationships
    entry = relationship("Entry", back_populates="maneuvers")

    # Fields
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    entry_id = Column(
        Integer, ForeignKey("entry.id"), index=True, doc="ID of the parent Entry row in database"
    )
    maneuver_type = Column(
        Text,
        index=True,
        nullable=True,
        doc="Type of maneuver performed to separate from entry vehicle.",
    )
    time_man = Column(
        Integer, nullable=True, doc="Time that spacecraft performs maneuver in seconds past J2000."
    )
    dv_maneuver_x = Column(Float, index=True, nullable=True, doc="Delta V of maneuver [km/s] in X.")
    dv_maneuver_y = Column(Float, index=True, nullable=True, doc="Delta V of maneuver [km/s] in Y.")
    dv_maneuver_z = Column(Float, index=True, nullable=True, doc="Delta V of maneuver [km/s] in Z.")
    dv_maneuver_mag = Column(
        Float, index=True, nullable=True, doc="Delta V of maneuver [km/s] magnitude."
    )
    pos_man_x = Column(
        Float, nullable=True, doc="x component of spacecraft position at time of maneuver [km]."
    )
    pos_man_y = Column(
        Float, nullable=True, doc="y component of spacecraft position at time of maneuver [km]."
    )
    pos_man_z = Column(
        Float, nullable=True, doc="z component of spacecraft position at time of maneuver [km]."
    )
    vel_man_x = Column(
        Float, nullable=True, doc="x component of spacecraft velocity at time of maneuver [km/s]."
    )
    vel_man_y = Column(
        Float, nullable=True, doc="y component of spacecraft velocity at time of maneuver [km/s]."
    )
    vel_man_z = Column(
        Float, nullable=True, doc="z component of spacecraft velocity at time of maneuver [km/s]."
    )


class Occultation(Base):
    # Identity
    __tablename__ = "occultation"

    # Relationships
    trajectory = relationship("Trajectory", back_populates="occultations")

    # Fields
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    trajectory_id = Column(
        Integer, ForeignKey("trajectory.id"), index=True, doc="SQL ID of the parent trajectory"
    )
    t_occ_in = Column(
        Integer,
        nullable=True,
        doc="Time that spacecraft enters into occultation relative to the Earth in seconds past J2000.",
    )
    t_occ_out = Column(
        Integer,
        nullable=True,
        doc="Time that spacecraft exits occultation relative to the Earth in seconds past J2000.",
    )


class Trajectory(Base):
    # Identity
    __tablename__ = "trajectory"

    # Relationships
    target_body = relationship("Body", back_populates="trajectories")
    architecture = relationship("Architecture")
    entries = relationship("Entry", back_populates="trajectory")
    occultations = relationship("Occultation", back_populates="trajectory")
    flybys = relationship("Flyby", back_populates="trajectory", order_by="Flyby.order")

    # Fields
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    body_id = Column(Integer, ForeignKey("body.id"), index=True, doc="SQL body ID")
    architecture_id = Column(
        Integer, ForeignKey("architecture.id"), index=True, doc="SQL architecture ID"
    )
    t_launch = Column(Integer, index=True, doc="Time of launch in seconds past J2000")
    t_arr = Column(Integer, index=True, doc="Time of target arrival in seconds past J2000")
    v_inf_arr_x = Column(
        Float, index=True, doc="x component of interplanetary arrival velocity at target [km/s]"
    )
    v_inf_arr_y = Column(
        Float, index=True, doc="y component of interplanetary arrival velocity at target [km/s]"
    )
    v_inf_arr_z = Column(
        Float, index=True, doc="z component of interplanetary arrival velocity at target [km/s]"
    )
    v_inf_arr_mag = Column(
        Float, index=True, doc="magnitude of interplanetary arrival velocity at target [km/s]"
    )
    c3 = Column(Float, index=True, doc="Characteristic energy of launch [km^2/s^2]")
    interplanetary_dv = Column(
        Float, index=True, doc="total DeltaV required for interplanetary trajectory [km/s]"
    )
    solar_phase_angle = Column(
        Float, index=True, nullable=True, doc="Sun-Target-Vinfinity Angle at arrival"
    )
    solar_conj_angle = Column(
        Float, index=True, nullable=True, doc="Sun-Target-Earth Angle at arrival"
    )
    solar_incidence_angle = Column(
        Float, index=True, nullable=True, doc="Sun-Target-Entry Position Angle at arrival"
    )
    pos_earth_arr_x = Column(Float, doc="x component of Earth position at time of arrival [km]")
    pos_earth_arr_y = Column(Float, doc="y component of Earth position at time of arrival [km]")
    pos_earth_arr_z = Column(Float, doc="z component of Earth position at time of arrival [km]")
    pos_earth_arr_lat = Column(Float, doc="latitude of Earth in body frame at time of arrival")
    pos_earth_arr_lon = Column(Float, doc="longitude of Earth in body frame at time of arrival")
    pos_sc_arr_x = Column(Float, doc="x component of spacecraft position at time of arrival [km]")
    pos_sc_arr_y = Column(Float, doc="y component of spacecraft position at time of arrival [km]")
    pos_sc_arr_z = Column(Float, doc="z component of spacecraft position at time of arrival [km]")
    pos_target_arr_x = Column(Float, doc="x component of target position at time of arrival [km]")
    pos_target_arr_y = Column(Float, doc="y component of target position at time of arrival [km]")
    pos_target_arr_z = Column(Float, doc="z component of target position at time of arrival [km]")
    pos_sun_arr_lat = Column(Float, doc="latitude of Sun in body frame at time of arrival")
    pos_sun_arr_lon = Column(Float, doc="longitude of Sun in body frame at time of arrival")
