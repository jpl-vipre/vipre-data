import typing
from enum import Enum

from pydantic import BaseModel, Field


class FilterCategory(str, Enum):
    CHECKBOX = "checkbox"
    VALUE = "value"
    RANGE = "range"


class Filter(BaseModel):
    display_name: str
    field_name: str
    category: FilterCategory = Field(FilterCategory.RANGE)


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
    category: FilterCategory.RANGE


class FilterCheckboxRequest(FilterRequest):
    checked: bool
    category = FilterCategory.CHECKBOX


class FilterValueRequest(FilterRequest):
    value: typing.Union[number, str]
    category = FilterCategory.VALUE


class TrajectoryRequest(BaseModel):
    filters: list[typing.Union[FilterRangeRequest, FilterCheckboxRequest, FilterValueRequest]]
    fields: typing.Optional[list[str]]
