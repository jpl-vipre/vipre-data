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
from enum import Enum

import numpy as np
from pydantic import BaseModel


class FilterCategory(str, Enum):
    CHECKBOX = "checkbox"
    VALUE = "value"
    SLIDER = "slider"


class Filter(BaseModel):
    display_name: str
    field_name: str
    category: FilterCategory = FilterCategory.SLIDER


def _vector_filters(desc, name):
    return [
        Filter(display_name=f"{desc} [{c.capitalize()}]", field_name=f"{name}_{c}") for c in "xyz"
    ]


# TODO: Add architecture ID?
TrajectoryFilters: list[Filter] = [
    Filter(display_name="Launch Date", field_name="t_launch"),
    Filter(display_name="Arrival Date", field_name="t_arr"),
    *_vector_filters("Arrival V Infinity Vector", "v_inf_arr"),
    *_vector_filters("Earth position at time of arrival", "pos_earth_arr"),
    *_vector_filters("Spacecraft position at time of arrival", "pos_sc_arr"),
    *_vector_filters("Target position at time of arrival", "pos_target_arr"),
    Filter(display_name="Launch C3", field_name="c3"),
    Filter(display_name="Total Cruise DeltaV", field_name="dv_total"),
]
trajectory_filter_fields = {f.field_name for f in TrajectoryFilters}

EntryFilters: list[Filter] = [
    Filter(display_name="B-Plane vector angle", field_name="bvec_theta"),
    Filter(display_name="B-Plane vector magnitude", field_name="bvec_mag"),
    Filter(display_name="Safe Entry Trajectory Flag", field_name="safe"),
    Filter(display_name="Time of Entry", field_name="t_entry"),
    *_vector_filters("Spacecraft Position @ entry", "pos_entry"),
    *_vector_filters("Spacecraft Velocity @ entry", "vel_entry"),
    Filter(display_name="Relay Data Volume", field_name="relay_volume"),
    Filter(display_name="Flight Path Angle", field_name="flight_path_angle"),
]
entry_filter_fields = {f.field_name for f in EntryFilters}

number = t.Union[int, float]


class LatLong(BaseModel):
    latitude: float
    longitude: float


class LatLongH(LatLong):
    height: float


Coord = tuple[float, float, float]


class ConicParams(BaseModel):
    pos_i: Coord
    vel_i: Coord
    time_i: float

    pos_f: Coord
    vel_f: Coord
    time_f: float

    ta_step: int
    mu: float
    rev_check: bool = False
    time_flag: bool = False


def get_xyz_tuple(obj: object, field_name: str) -> np.ndarray:
    """
    Create x, y, z tuples from an object based on field name.
    The object is expected to have attributes with "<field_name>_{x,y,z}".

    :param obj: python object with fields mapping to xyz coordinates ("_x", "_y", "_z")
    :param field_name: prefix of the fields with xzy coordinates
    :return: numpy array of shape (1,3,1)
    """
    assert all(
        hasattr(obj, f"{field_name}_{i}") for i in "xyz"
    ), f"Field: {field_name} does not exist on object: {obj}"
    return np.array([[[getattr(obj, f"{field_name}_{i}")] for i in "xyz"]])


def make_lat_long(height: np.ndarray, lat: np.ndarray, lon: np.ndarray) -> list[LatLongH]:
    """

    :param lat:
    :param lon:
    :param height:

    :return:
    """
    fields = ["height", "latitude", "longitude"]
    points = np.array([height, lat, lon]).T.reshape(-1, 3)
    return [LatLongH(**{k: v for k, v in zip(fields, point)}) for point in points]
