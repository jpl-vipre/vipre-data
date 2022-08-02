import typing as t

from pydantic import BaseModel as PydanticBaseModel, validator, root_validator
import numpy as np

from .utils import Filter


def calculate_magnitudes(cls, values: dict) -> dict:
    """Calculate the value for any fields named "*_mag" based on presence of "_x", "_y", "_z" fields.

    :param values: Dict with values for the class - should have 3 component attributes
                   ("{field}_{x,y,z}") for each "{field}_mag" field.
    :return: Original values with the _mag fields populated based on linalg.norm calculation
    """
    # Assume presence of a "*_mag" field indicates a vector property for which the x, y, z components will exist
    mag_fields = [v for v in values if v.endswith("_mag")]
    for field_name in mag_fields:
        root = field_name[:-4]
        try:
            vectors = [values[f"{root}_{c}"] for c in {"x", "y", "z"}]
        except AttributeError:
            # Missing x,y,z components for a _mag field is not catastrophic
            continue
        else:
            # Successfully calculated the magnitude so safe to write to the field
            values[field_name] = np.linalg.norm(vectors)
    return values


class BaseModel(PydanticBaseModel):
    _calculate_magnitudes = root_validator(allow_reuse=True, pre=False)(calculate_magnitudes)


class FieldsResponse(BaseModel):
    TrajectoryFields: list[str]
    EntryFields: list[str]


class FiltersResponse(BaseModel):
    TrajectoryFilters: list[Filter]
    EntryFilters: list[Filter]


class BodySummary(BaseModel):
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


class Architecture(BaseModel):
    sequence: t.Optional[str]

    class Config:
        orm_mode = True


class Maneuver(BaseModel):
    id: t.Optional[int]
    maneuver_type: t.Optional[str]
    dv_maneuver: t.Optional[float]

    class Config:
        orm_mode = True


class Occultation(BaseModel):
    id: t.Optional[int]

    class Config:
        orm_mode = True


class Flyby(BaseModel):
    flyby_body: Body
    order: int
    t_flyby: float

    class Config:
        orm_mode = True


class TrajectorySummary(BaseModel):
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


class Entry(BaseModel):
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
