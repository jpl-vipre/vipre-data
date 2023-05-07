# Copyright (c) 2021-2023 California Institute of Technology ("Caltech"). U.S.
# Government sponsorship acknowledged.
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Caltech nor its operating division, the Jet Propulsion
#   Laboratory, nor the names of its contributors may be used to endorse or
#   promote products derived from this software without specific prior written
#   permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from typing import Type

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text, Float, inspect, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

VERSION = "1.0.0"

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
    radius = Column(Float, doc="mean radius of body")
    mu = Column(Float, doc="gravity parameter")
    period = Column(Float, doc="body rotational period")
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
        doc="Down sampled time in datarate time series. Time is seconds after entry",
    )
    rate = Column(Float, nullable=True, doc="Down sampled datarate in datarate time series")


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
    bvec_theta = Column(Float, index=True, doc="Angle on B-plane for target arrival")
    bvec_mag = Column(Float, index=True, doc="Radial distance from body origin for target arrival")
    safe = Column(
        Boolean,
        doc="Flag indicating whether trajectory avoids unsafe conditions (ring impact, etc)",
    )
    t_entry = Column(Integer, index=True, doc="Time of atmospheric entry in seconds past J2000")
    pos_entry_x = Column(
        Float, nullable=True, doc="x component of spacecraft position at time of entry"
    )
    pos_entry_y = Column(
        Float, nullable=True, doc="y component of spacecraft position at time of entry"
    )
    pos_entry_z = Column(
        Float, nullable=True, doc="z component of spacecraft position at time of entry"
    )
    pos_entry_mag = Column(
        Float, index=True, nullable=True, doc="magnitude of spacecraft position at time of entry"
    )
    pos_entry_lat = Column(
        Float, index=True, nullable=True, doc="latitude of spacecraft position at time of entry"
    )
    pos_entry_lon = Column(
        Float, nullable=True, doc="longitude of spacecraft position at time of entry"
    )
    vel_entry_x = Column(
        Float,
        nullable=True,
        doc="X component of spacecraft relative entry velocity at time of entry",
    )
    vel_entry_y = Column(
        Float,
        nullable=True,
        doc="y component of spacecraft relative entry velocity at time of entry",
    )
    vel_entry_z = Column(
        Float,
        nullable=True,
        doc="z component of spacecraft relative entry velocity at time of entry",
    )
    vel_entry_mag = Column(
        Float,
        index=True,
        nullable=True,
        doc="magnitude of spacecraft relative entry velocity at time of entry",
    )
    vel_entry_dec = Column(
        Float,
        index=True,
        nullable=True,
        doc="declination of spacecraft relative entry velocity at time of entry",
    )
    vel_entry_ra = Column(
        Float,
        index=True,
        nullable=True,
        doc="right ascension of spacecraft relative entry velocity at time of entry",
    )
    flight_path_angle = Column(
        Float, index=True, nullable=True, doc="flight path angle at point of entry"
    )
    solar_phase_angle = Column(Float, index=True, nullable=True, doc="Sun-Target-V-infinity Angle")
    solar_conj_angle = Column(Float, index=True, nullable=True, doc="Sun-Target-Earth Angle")
    solar_incidence_angle = Column(
        Float, index=True, nullable=True, doc="Sun-Target-Entry Position Angle"
    )
    pos_sun_entry_x = Column(
        Float, nullable=True, doc="x component of sun position at time of entry"
    )
    pos_sun_entry_y = Column(
        Float, nullable=True, doc="y component of sun position at time of entry"
    )
    pos_sun_entry_z = Column(
        Float, nullable=True, doc="z component of sun position at time of entry"
    )
    pos_earth_entry_x = Column(
        Float, nullable=True, doc="x component of Earth position at time of entry"
    )
    pos_earth_entry_y = Column(
        Float, nullable=True, doc="y component of Earth position at time of entry"
    )
    pos_earth_entry_z = Column(
        Float, nullable=True, doc="z component of Earth position at time of entry"
    )
    pos_target_entry_x = Column(
        Float, nullable=True, doc="x component of target position at time of entry"
    )
    pos_target_entry_y = Column(
        Float, nullable=True, doc="y component of target position at time of entry"
    )
    pos_target_entry_z = Column(
        Float, nullable=True, doc="z component of target position at time of entry"
    )
    rot_vel_entry_x = Column(
        Float,
        nullable=True,
        doc="X component of spacecraft relative entry velocity at time of entry in planet rotating frame",
    )
    rot_vel_entry_y = Column(
        Float,
        nullable=True,
        doc="y component of spacecraft relative entry velocity at time of entry in planet rotating frame",
    )
    rot_vel_entry_z = Column(
        Float,
        nullable=True,
        doc="z component of spacecraft relative entry velocity at time of entry in planet rotating frame",
    )
    rot_vel_entry_mag = Column(
        Float,
        index=True,
        nullable=True,
        doc="magnitude of spacecraft relative entry velocity at time of entry in planet rotating frame",
    )
    rot_vel_entry_dec = Column(
        Float,
        index=True,
        nullable=True,
        doc="declination of spacecraft relative entry velocity at time of entry in planet rotating frame",
    )
    rot_vel_entry_ra = Column(
        Float,
        index=True,
        nullable=True,
        doc="right ascension of spacecraft relative entry velocity at time of entry in planet rotating frame",
    )
    relay_volume = Column(
        Float, index=True, nullable=True, doc="Total data volume relayable by entry vehicle."
    )
    ring_shadow = Column(
        Boolean,
        index=True,
        nullable=True,
        doc="true if the entry is in the shadow of a planet's ring",
    )
    carrier_orbit = Column(
        Text,
        index=True,
        nullable=True,
        doc="label describing the pre-divert orbit. Primarily used to distinguish between flyby and orbiting probe releases.",
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
    altitude = Column(Float, doc="Altitude above flyby body surface at flyby hyperbola periapsis")
    v_inf_in_x = Column(Float, doc="x component of incoming flyby v_infinity")
    v_inf_in_y = Column(Float, doc="y component of incoming flyby v_infinity")
    v_inf_in_z = Column(Float, doc="z component of incoming flyby v_infinity")
    v_inf_in_mag = Column(Float, doc="magnitude component of incoming flyby v_infinity")
    v_inf_out_x = Column(Float, doc="x component of outgoing flyby v_infinity")
    v_inf_out_y = Column(Float, doc="y component of outgoing flyby v_infinity")
    v_inf_out_z = Column(Float, doc="z component of outgoing flyby v_infinity")
    v_inf_out_mag = Column(Float, doc="magnitude of outgoing flyby v_infinity")


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
        Text, nullable=True, doc="Type of maneuver performed to separate from entry vehicle."
    )
    time_man = Column(
        Integer, nullable=True, doc="Time that spacecraft performs maneuver in seconds past J2000."
    )
    dv_maneuver_x = Column(Float, nullable=True, doc="Delta V of maneuver in X.")
    dv_maneuver_y = Column(Float, nullable=True, doc="Delta V of maneuver in Y.")
    dv_maneuver_z = Column(Float, nullable=True, doc="Delta V of maneuver in Z.")
    dv_maneuver_mag = Column(Float, index=True, nullable=True, doc="Delta V of maneuver magnitude.")
    pos_man_x = Column(
        Float, nullable=True, doc="x component of spacecraft position at time of maneuver."
    )
    pos_man_y = Column(
        Float, nullable=True, doc="y component of spacecraft position at time of maneuver."
    )
    pos_man_z = Column(
        Float, nullable=True, doc="z component of spacecraft position at time of maneuver."
    )
    vel_man_x = Column(
        Float, nullable=True, doc="x component of spacecraft velocity at time of maneuver."
    )
    vel_man_y = Column(
        Float, nullable=True, doc="y component of spacecraft velocity at time of maneuver."
    )
    vel_man_z = Column(
        Float, nullable=True, doc="z component of spacecraft velocity at time of maneuver."
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
    v_inf_arr_x = Column(Float, doc="x component of interplanetary arrival velocity at target")
    v_inf_arr_y = Column(Float, doc="y component of interplanetary arrival velocity at target")
    v_inf_arr_z = Column(Float, doc="z component of interplanetary arrival velocity at target")
    v_inf_arr_mag = Column(
        Float, index=True, doc="magnitude of interplanetary arrival velocity at target"
    )
    v_inf_arr_dec = Column(
        Float, index=True, doc="declination of interplanetary arrival velocity at target"
    )
    v_inf_arr_ra = Column(
        Float, index=True, doc="right ascension of interplanetary arrival velocity at target"
    )
    c3 = Column(Float, index=True, doc="Characteristic energy of launch")
    interplanetary_dv = Column(
        Float, index=True, doc="total DeltaV required for interplanetary trajectory"
    )
    solar_phase_angle = Column(
        Float, index=True, nullable=True, doc="Sun-Target-V-infinity Angle at arrival"
    )
    solar_conj_angle = Column(
        Float, index=True, nullable=True, doc="Sun-Target-Earth Angle at arrival"
    )
    solar_incidence_angle = Column(
        Float, index=True, nullable=True, doc="Sun-Target-Entry Position Angle at arrival"
    )
    pos_earth_arr_x = Column(Float, doc="x component of Earth position at time of arrival")
    pos_earth_arr_y = Column(Float, doc="y component of Earth position at time of arrival")
    pos_earth_arr_z = Column(Float, doc="z component of Earth position at time of arrival")
    pos_earth_arr_lat = Column(
        Float, index=True, doc="latitude of Earth in body frame at time of arrival"
    )
    pos_earth_arr_lon = Column(
        Float, index=True, doc="longitude of Earth in body frame at time of arrival"
    )
    pos_sc_arr_x = Column(Float, doc="x component of spacecraft position at time of arrival")
    pos_sc_arr_y = Column(Float, doc="y component of spacecraft position at time of arrival")
    pos_sc_arr_z = Column(Float, doc="z component of spacecraft position at time of arrival")
    pos_target_arr_x = Column(Float, doc="x component of target position at time of arrival")
    pos_target_arr_y = Column(Float, doc="y component of target position at time of arrival")
    pos_target_arr_z = Column(Float, doc="z component of target position at time of arrival")
    pos_sun_arr_lat = Column(
        Float, index=True, doc="latitude of Sun in body frame at time of arrival"
    )
    pos_sun_arr_lon = Column(
        Float, index=True, doc="longitude of Sun in body frame at time of arrival"
    )
