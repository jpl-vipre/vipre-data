from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Trajectory(Base):
    __tablename__ = "trajectories"
    id = Column(Integer, primary_key=True)
    body = relationship("Body", back_populates="trajectories")
    source = relationship("DataSource", back_populates="trajectories")

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


class Trip(Base):
    __tablename__ = "trips"
    body = relationship("Body", back_populates="trips")

    launch_days = Column(Integer)
    arrive_days = Column(Integer)

    v_inf_x = Column(Float)
    v_inf_y = Column(Float)
    v_inf_z = Column(Float)

    planet_pos_x = Column(Float)
    planet_pos_y = Column(Float)
    planet_pos_z = Column(Float)

    planet_vel_x = Column(Float)
    planet_vel_y = Column(Float)
    planet_vel_z = Column(Float)

    c3 = Column(Float)
    delta_v = Column(Float)
    arrival_mass = Column(Float)
    flyby_body = Column(String)


class Body(Base):
    __tablename__ = "bodies"
    name = Column(String, primary_key=True)
    trajectories = relationship("Trajectory", back_populates="body")
    trips = relationship("Trip", back_populates="body")


class DataSource(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    trajectories = relationship("Trajectory", back_populates="source")

    body = Column(String)
    hEntry = Column(Integer)
    vId = Column(Integer)
    fileName = Column(String)
