import typing as t

from pydantic import BaseModel, validator, root_validator
import numpy as np

from .utils import Filter, LatLongH, make_lat_long
from vipre_data.computations.cart2sph import cart2sph


def calculate_magnitudes(cls, values: dict) -> dict:
    """Calculate the value for any fields named "*_mag" based on presence of "_x", "_y", "_z" fields.

    :param values: Dict with values for the class - should have 3 component attributes
                   ("{field}_{x,y,z}") for each "{field}_mag" field.
    :return: Original values with the _mag fields populated based on linalg.norm calculation
    """
    # Assume presence of a "*_mag" field indicates a vector property for which the x, y, z components will exist
    mag_fields = [v for v in values if v.endswith("_mag")]
    for field_name in mag_fields:
        if values[field_name]:
            continue  # Field is already populated and should not be overwritten
        root = field_name[:-4]  # dTrim off "_mag" to get root name
        try:
            vectors = [values[f"{root}_{c}"] for c in "xyz"]
            values[field_name] = np.linalg.norm(vectors)
            # TODO: check for None values (missing vector components)
        except KeyError:
            # Missing x,y,z components for a _mag field is not catastrophic
            continue
        except TypeError:
            # Unable to calculate magnitude, one of the components may be None
            continue
    return values


class DbModelBase(BaseModel):
    _calculate_magnitudes = root_validator(allow_reuse=True, pre=False)(calculate_magnitudes)

    class Config:
        orm_mode = True
        extra = "allow"


class FieldsResponse(BaseModel):
    TrajectoryFields: list[str]
    EntryFields: list[str]


class FiltersResponse(BaseModel):
    TrajectoryFilters: list[Filter]
    EntryFilters: list[Filter]


class DbInfo(BaseModel):
    database: str
    tables: list[str]
    schema_version: str


class TrajectoryArcs(BaseModel):
    carrier: list[LatLongH]
    probe: list[LatLongH]


class BodySummary(DbModelBase):
    id: t.Optional[int]
    name: t.Optional[str]


class Body(BodySummary):
    radius: float
    mu: float
    period: float
    pole_vec_x: float
    pole_vec_y: float
    pole_vec_z: float


class Architecture(DbModelBase):
    sequence: t.Optional[str]


class Maneuver(DbModelBase):
    id: t.Optional[int]

    maneuver_type: t.Optional[str]
    time_man: t.Optional[int]

    dv_maneuver_x: t.Optional[float]
    dv_maneuver_y: t.Optional[float]
    dv_maneuver_z: t.Optional[float]
    dv_maneuver_mag: t.Optional[float]

    pos_man_x: t.Optional[float]
    pos_man_y: t.Optional[float]
    pos_man_z: t.Optional[float]
    vel_man_x: t.Optional[float]
    vel_man_y: t.Optional[float]
    vel_man_z: t.Optional[float]


class DataRate(DbModelBase):
    id: t.Optional[int]
    entry_id: t.Optional[int]
    order: t.Optional[int]
    time: t.Optional[int]
    rate: t.Optional[float]


class Occultation(DbModelBase):
    id: t.Optional[int]


class Flyby(DbModelBase):
    flyby_body: Body
    order: int
    t_flyby: float


class TrajectorySummary(DbModelBase):
    id: t.Optional[int]

    t_launch: t.Optional[float]
    interplanetary_dv: t.Optional[float]

    v_inf_arr_x: t.Optional[float]
    v_inf_arr_y: t.Optional[float]
    v_inf_arr_z: t.Optional[float]
    v_inf_arr_mag: t.Optional[float]

    t_arr: t.Optional[float]
    c3: t.Optional[float]


class Trajectory(TrajectorySummary):
    pos_earth_arr_x: t.Optional[float]
    pos_earth_arr_y: t.Optional[float]
    pos_earth_arr_z: t.Optional[float]
    pos_earth_arr_mag: t.Optional[float]
    pos_earth_arr_lat: t.Optional[float]
    pos_earth_arr_lon: t.Optional[float]

    pos_sc_arr_x: t.Optional[float]
    pos_sc_arr_y: t.Optional[float]
    pos_sc_arr_z: t.Optional[float]
    pos_sc_arr_mag: t.Optional[float]

    pos_target_arr_x: t.Optional[float]
    pos_target_arr_y: t.Optional[float]
    pos_target_arr_z: t.Optional[float]
    pos_target_arr_mag: t.Optional[float]

    solar_phase_angle: t.Optional[float]
    solar_conj_angle: t.Optional[float]
    solar_incidence_angle: t.Optional[float]

    pos_sun_arr_lat: t.Optional[float]
    pos_sun_arr_lon: t.Optional[float]


class TrajectoryFull(Trajectory):
    target_body: t.Optional[Body]
    architecture: t.Optional[Architecture]
    occultations: t.Optional[list[Occultation]]
    flybys: t.Optional[list[Flyby]]


class Entry(DbModelBase):
    id: t.Optional[int]

    target_body: t.Optional[Body]

    bvec_theta: t.Optional[float]
    bvec_mag: t.Optional[float]
    safe: t.Optional[bool]
    t_entry: t.Optional[int]
    relay_volume: t.Optional[float]

    pos_entry_x: t.Optional[float]
    pos_entry_y: t.Optional[float]
    pos_entry_z: t.Optional[float]
    pos_entry_mag: t.Optional[float]

    vel_entry_x: t.Optional[float]
    vel_entry_y: t.Optional[float]
    vel_entry_z: t.Optional[float]
    vel_entry_mag: t.Optional[float]
    pos_entry_lat: t.Optional[float]
    pos_entry_lon: t.Optional[float]
    # pos_entry_height: t.Optional[float]

    rot_vel_entry_x: t.Optional[float]
    rot_vel_entry_y: t.Optional[float]
    rot_vel_entry_z: t.Optional[float]
    rot_vel_entry_mag: t.Optional[float]

    flight_path_angle: t.Optional[float]
    solar_phase_angle: t.Optional[float]
    solar_conj_angle: t.Optional[float]
    solar_incidence_angle: t.Optional[float]

    # @root_validator(pre=False)
    # def make_height(cls, values):
    #     pos = np.array([values["pos_entry_lat"], values["pos_entry_lon"]])
    #     if all(pos):  # Confirm that lat/lon are available
    #         values["pos_entry_height"] = np.linalg.norm(pos)
    #     return values


class EntryFull(Entry):
    trajectory: t.Optional[Trajectory]
    maneuvers: t.Optional[list[Maneuver]]
    datarates: t.Optional[list[DataRate]]

    pos_sun_entry_x: t.Optional[float]
    pos_sun_entry_y: t.Optional[float]
    pos_sun_entry_z: t.Optional[float]
    pos_sun_entry_mag: t.Optional[float]

    pos_earth_entry_x: t.Optional[float]
    pos_earth_entry_y: t.Optional[float]
    pos_earth_entry_z: t.Optional[float]
    pos_earth_entry_mag: t.Optional[float]

    pos_target_entry_x: t.Optional[float]
    pos_target_entry_y: t.Optional[float]
    pos_target_entry_z: t.Optional[float]
    pos_target_entry_mag: t.Optional[float]

    ring_shadow: t.Optional[bool]
    carrier_orbit: t.Optional[str]
