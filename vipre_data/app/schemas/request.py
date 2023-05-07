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
    limit: conint(gt=0, le=10000) = 100


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
    probe_ta_step: conint(ge=15, le=100) = 25
    carrier_ta_step: conint(ge=15, le=5000) = 500
