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
        root = field_name[:-4]  # Trim off "_mag" to get root name
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


class FieldsResponse(BaseModel):
    TrajectoryFields: list[str]
    EntryFields: list[str]


class FiltersResponse(BaseModel):
    TrajectoryFilters: list[Filter]
    EntryFilters: list[Filter]


class TrajectoryArcs(BaseModel):
    carrier: list[LatLongH]
    probe: list[LatLongH]


class BodySummary(DbModelBase):
    id: t.Optional[int]
    name: t.Optional[str]

    class Config:
        orm_mode = True
        extra = "allow"


class Body(BodySummary):
    radius: float
    mu: float
    period: float
    pole_vec_x: float
    pole_vec_y: float
    pole_vec_z: float


class Architecture(DbModelBase):
    sequence: t.Optional[str]

    class Config:
        orm_mode = True


class Maneuver(DbModelBase):
    id: t.Optional[int]
    maneuver_type: t.Optional[str]
    dv_maneuver: t.Optional[float]

    class Config:
        orm_mode = True


class Occultation(DbModelBase):
    id: t.Optional[int]

    class Config:
        orm_mode = True


class Flyby(DbModelBase):
    flyby_body: Body
    order: int
    t_flyby: float

    class Config:
        orm_mode = True


class TrajectorySummary(DbModelBase):
    id: t.Optional[int]

    t_launch: t.Optional[float]
    dv_total: t.Optional[float]

    v_inf_arr_x: t.Optional[float]
    v_inf_arr_y: t.Optional[float]
    v_inf_arr_z: t.Optional[float]
    v_inf_arr_mag: t.Optional[float]

    t_arr: t.Optional[float]
    c3: t.Optional[float]

    class Config:
        orm_mode = True
        extra = "allow"


class Trajectory(TrajectorySummary):
    pos_earth_arr_x: t.Optional[float]
    pos_earth_arr_y: t.Optional[float]
    pos_earth_arr_z: t.Optional[float]
    pos_earth_arr_mag: t.Optional[float]

    pos_sc_arr_x: t.Optional[float]
    pos_sc_arr_y: t.Optional[float]
    pos_sc_arr_z: t.Optional[float]
    pos_sc_arr_mag: t.Optional[float]

    pos_target_arr_x: t.Optional[float]
    pos_target_arr_y: t.Optional[float]
    pos_target_arr_z: t.Optional[float]
    pos_target_arr_mag: t.Optional[float]


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
    pos_entry_latitude: t.Optional[float]
    pos_entry_longitude: t.Optional[float]
    pos_entry_height: t.Optional[float]

    flight_path_angle: t.Optional[float]

    @root_validator(pre=False)
    def make_lat_long(cls, values):
        pos = np.array([[values[f"pos_entry_{c}"]] for c in "xyz"])
        lat_long = make_lat_long(*cart2sph(*pos))[0]
        for i, c in enumerate(["latitude", "longitude", "height"]):
            values[f"pos_entry_{c}"] = lat_long.dict()[c]
        return values

    class Config:
        orm_mode = True


class EntryFull(Entry):
    trajectory: t.Optional[Trajectory]
    maneuvers: t.Optional[list[Maneuver]]

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
