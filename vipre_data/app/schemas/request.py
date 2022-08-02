import typing as t

from pydantic import BaseModel, conint

from .utils import FilterCategory, number


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


class EntryArcRequest(BaseModel):
    ta_step: conint(gt=15, le=100) = 25
