import typing as t
from enum import Enum

from pydantic import BaseModel, conint


class FilterCategory(str, Enum):
    CHECKBOX = "checkbox"
    VALUE = "value"
    SLIDER = "slider"


class Filter(BaseModel):
    display_name: str
    field_name: str
    category: FilterCategory = FilterCategory.SLIDER


TrajectoryFilters: list[Filter] = [
    Filter(display_name="Launch Date", field_name="t_launch"),
    Filter(display_name="Arrival Date", field_name="t_arr"),
    Filter(display_name="Arrival V Infinity Vector X", field_name="v_inf_arr_x"),
    Filter(display_name="Arrival V Infinity Vector X", field_name="v_inf_arr_y"),
    Filter(display_name="Arrival V Infinity Vector X", field_name="v_inf_arr_z"),
    Filter(display_name="Launch C3", field_name="c3"),
    Filter(display_name="Total Cruise DeltaV", field_name="dv_total"),
]
trajectory_filter_fields = {f.field_name for f in TrajectoryFilters}

EntryFilters: list[Filter] = [
    Filter(display_name="B-Plane vector angle", field_name="bvec_theta"),
    Filter(display_name="B-Plane vector magnitude", field_name="bvec_mag"),
    Filter(display_name="Safe Entry Trajectory Flag", field_name="safe"),
    Filter(display_name="Time of Entry", field_name="t_entry"),
    Filter(display_name="Spacecraft Position @ entry X", field_name="pos_entry_x"),
    Filter(display_name="Spacecraft Position @ entry Y", field_name="pos_entry_y"),
    Filter(display_name="Spacecraft Position @ entry Z", field_name="pos_entry_z"),
    Filter(display_name="Spacecraft Velocity @ entry X", field_name="vel_entry_x"),
    Filter(display_name="Spacecraft Velocity @ entry Y", field_name="vel_entry_y"),
    Filter(display_name="Spacecraft Velocity @ entry Y", field_name="vel_entry_z"),
    Filter(display_name="Relay Data Volume", field_name="relay_volume"),
]
entry_filter_fields = {f.field_name for f in EntryFilters}


class FiltersResponse(BaseModel):
    TrajectoryFilters: list[Filter]
    EntryFilters: list[Filter]


class FieldsResponse(BaseModel):
    TrajectoryFields: list[str]
    EntryFields: list[str]


number = t.Union[int, float]


class FilterRequest(BaseModel):
    field_name: str
    category: FilterCategory


class FilterRangeRequest(FilterRequest):
    lower: number
    upper: number
    category: t.Literal[FilterCategory.SLIDER]


class FilterCheckboxRequest(FilterRequest):
    checked: bool
    category: t.Literal[FilterCategory.CHECKBOX]


class FilterValueRequest(FilterRequest):
    value: t.Union[number, str]
    category: t.Literal[FilterCategory.VALUE]


Filters = list[t.Union[FilterRangeRequest, FilterCheckboxRequest, FilterValueRequest]]


class DataRequest(BaseModel):
    filters: Filters
    fields: t.Optional[list[str]]
    limit: conint(gt=0, le=1000) = 100


class TrajectoryRequest(DataRequest):
    class Config:
        schema_extra = {
            "example": {
                "filters": [{"field_name": "c3", "category": "slider", "lower": 97, "upper": 99}],
                "fields": ["id", "c3", "dv_total", "t_launch"],
                "limit": 100,
            }
        }


class EntryRequest(DataRequest):
    class Config:
        schema_extra = {
            "example": {
                "filters": [
                    {
                        "field_name": "bvec_mag",
                        "category": "slider",
                        "lower": 27000,
                        "upper": 270600,
                    }
                ],
                "fields": [
                    "id",
                    "bvec_theta",
                    "bvec_mag",
                    "t_entry",
                    "pos_entry_x",
                    "pos_entry_y",
                    "pos_entry_z",
                ],
                "limit": 100,
            }
        }


class Body(BaseModel):
    id: t.Optional[int]
    name: t.Optional[str]

    class Config:
        orm_mode = True
        extra = "allow"


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

    class Config:
        orm_mode = True
        extra = "allow"


class Trajectory(TrajectorySummary):

    target_body: t.Optional[Body]
    architecture: t.Optional[Architecture]
    occultations: t.Optional[list[Occultation]]
    flybys: t.Optional[list[Flyby]]

    t_arr: t.Optional[float]

    c3: t.Optional[float]


class TrajectoryFull(Trajectory):
    pos_earth_arr_x: t.Optional[float]
    pos_earth_arr_y: t.Optional[float]
    pos_earth_arr_z: t.Optional[float]

    pos_sc_arr_x: t.Optional[float]
    pos_sc_arr_y: t.Optional[float]
    pos_sc_arr_z: t.Optional[float]

    pos_target_arr_x: t.Optional[float]
    pos_target_arr_y: t.Optional[float]
    pos_target_arr_z: t.Optional[float]

    class Config:
        orm_mode = True


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

    vel_entry_x: t.Optional[float]
    vel_entry_y: t.Optional[float]
    vel_entry_z: t.Optional[float]

    class Config:
        orm_mode = True


class EntryFull(Entry):
    trajectory: t.Optional[Trajectory]
    maneuvers: t.Optional[list[Maneuver]]

    pos_sun_entry_x: t.Optional[float]
    pos_sun_entry_y: t.Optional[float]
    pos_sun_entry_z: t.Optional[float]

    pos_earth_entry_x: t.Optional[float]
    pos_earth_entry_y: t.Optional[float]
    pos_earth_entry_z: t.Optional[float]

    pos_target_entry_x: t.Optional[float]
    pos_target_entry_y: t.Optional[float]
    pos_target_entry_z: t.Optional[float]

    class Config:
        orm_mode = True
