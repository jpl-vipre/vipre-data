import typing
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


number = typing.Union[int, float]


class FilterRequest(BaseModel):
    field_name: str
    category: FilterCategory


class FilterRangeRequest(FilterRequest):
    lower: number
    upper: number
    category: typing.Literal[FilterCategory.SLIDER]


class FilterCheckboxRequest(FilterRequest):
    checked: bool
    category: typing.Literal[FilterCategory.CHECKBOX]


class FilterValueRequest(FilterRequest):
    value: typing.Union[number, str]
    category: typing.Literal[FilterCategory.VALUE]


Filters = list[typing.Union[FilterRangeRequest, FilterCheckboxRequest, FilterValueRequest]]


class DataRequest(BaseModel):
    filters: Filters
    fields: typing.Optional[list[str]]
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
                "filters": [{"field_name": "c3", "category": "slider", "lower": 97, "upper": 99}],
                "fields": ["id", "c3", "dv_total", "t_launch"],
                "limit": 100,
            }
        }


class Body(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        extra = "allow"


class Architecture(BaseModel):
    sequence: str

    class Config:
        orm_mode = True


class Entry(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Occultation(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Flyby(BaseModel):
    flyby_body: Body
    order: int
    t_flyby: float

    class Config:
        orm_mode = True


class Trajectory(BaseModel):
    id: int

    target_body: Body
    architecture: typing.Optional[Architecture]
    occultations: typing.Optional[list[Occultation]]
    flybys: typing.Optional[list[Flyby]]

    t_launch: typing.Optional[float]
    t_arr: typing.Optional[float]

    v_inf_arr_x: typing.Optional[float]
    v_inf_arr_y: typing.Optional[float]
    v_inf_arr_z: typing.Optional[float]

    c3: typing.Optional[float]
    dv_total: typing.Optional[float]

    pos_earth_x: typing.Optional[float]
    pos_earth_y: typing.Optional[float]
    pos_earth_z: typing.Optional[float]

    pos_sc_x: typing.Optional[float]
    pos_sc_y: typing.Optional[float]
    pos_sc_z: typing.Optional[float]

    pos_target_x: typing.Optional[float]
    pos_target_y: typing.Optional[float]
    pos_target_z: typing.Optional[float]

    class Config:
        orm_mode = True
        extra = "allow"
