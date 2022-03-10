from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    target_body = relationship("Body")
    trajectory = relationship("Trajectory", back_populates="entries")

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
    __tablename__ = "trajectories"
    target_body = relationship("Body", back_populates="trajectories")
    architecture = relationship("Architecture")

    launch_days = Column(Float)
    arrive_days = Column(Float)

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


class Body(Base):
    __tablename__ = "bodies"
    id = Column(Integer, primary_key=True)
    horizons_id = Column(Integer)
    name = Column(String)
    trajectories = relationship("Trajectory", back_populates="body")


class Flyby(Base):
    __tablename__ = "flybys"
    id = Column(Integer, primary_key=True)
    trajectory = relationship("Trajectory", back_populates="flybys")
    body = relationship("Body")
    days = Column(Integer)
    order = Column(Integer)

    # constrain unique(trajectory + order)

class Architecture(Base):
    __tablename__ = "architectures"
    id = Column(Integer, primary_key=True)
    sequence = Column(String)
