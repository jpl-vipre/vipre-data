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

import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from vipre_data.app import dependencies as deps
from vipre_data.app import schemas
from vipre_data.app.schemas.utils import get_xyz_tuple, make_lat_long
from vipre_data.computations.cart2sph import cart2sph
from vipre_data.computations.conic_1point import conic_1point
from vipre_data.computations.conic_2point import conic_2point
from vipre_data.sql import crud, models

router = APIRouter(
    prefix="/visualizations",
    tags=["visualizations"],
)


@router.post(
    "/trajectory_selection/{target_body_id}",
    response_model=list[schemas.response.Trajectory],
)
def trajectory_selection(
    target_body_id: int, req: schemas.request.TrajectoryRequest, db: Session = Depends(deps.get_db)
):
    result = crud.get_body_trajectories(db, target_body_id, filters=req.filters, limit=req.limit)
    return result


def get_carrier_arc(maneuver: models.Maneuver, ta_step: int, final_time: int):
    # TODO: Implement via conic_1point
    # Carrier velocity vector is sum of instantaneous velocity vector and delta_v of maneuver
    velocity_vector = get_xyz_tuple(maneuver, "vel_man")
    maneuver_dv = get_xyz_tuple(maneuver, "dv_maneuver")
    velocity_vector += maneuver_dv
    params = dict(
        r_1=get_xyz_tuple(maneuver, "pos_man"),
        v_1=velocity_vector,  # add dv_man to this v_1
        t_1=np.array([[maneuver.time_man]]),
        mu=maneuver.entry.target_body.mu,
        ta_step=ta_step,  # Just needs to be high enough for a smooth arc
        rev_check=0,  # Likely not ever changed by user
        time_flag=1,  # Likely not ever changed by user
    )
    pos_set, vel_set, time_set = conic_1point(**params)
    # pos_set: [ [[ x1, x2, ... ]], [[ y1, y2, ... ]], [[ z1, z2, ... ]] ]
    # vel_set: same...
    # time_set: [ [[ t1, t2, ... ]] ]

    # Identify last valid entry in time_set (all tuples up to final_time)
    final_idx = 0
    for i, time in enumerate(time_set.flatten()):
        if time >= final_time:
            final_idx = i
            break

    # slice each component (x,y,z) up to final_idx
    pos_set = pos_set[:, :, :final_idx]
    height, lat, long = cart2sph(*pos_set)

    return height, lat, long


def get_probe_arc(entry: models.Entry, maneuver: models.Maneuver, ta_step: int):
    params = dict(
        r_1=get_xyz_tuple(maneuver, "pos_man"),
        r_2=get_xyz_tuple(entry, "pos_entry"),
        v_1=get_xyz_tuple(maneuver, "vel_man"),
        v_2=get_xyz_tuple(entry, "vel_entry"),
        t_1=np.array([[maneuver.time_man]]),
        t_2=np.array([[entry.t_entry]]),
        mu=entry.target_body.mu,
        ta_step=ta_step,  # Just needs to be high enough for a smooth arc
        rev_check=0,  # Likely not ever changed by user
        time_flag=0,  # Likely not ever changed by user
    )
    pos_set, vel_set, time_set = conic_2point(**params)

    height, lat, long = cart2sph(*pos_set)
    return height, lat, long


@router.post("/get_entry_arc/{entry_id}", response_model=schemas.response.TrajectoryArcs)
def get_trajectory_arc(
    entry_id: int, req: schemas.request.EntryArcRequest, db: Session = Depends(deps.get_db)
):
    # Fetch required
    entry: models.Entry = db.query(models.Entry).where(models.Entry.id == entry_id).first()
    maneuver: models.Maneuver = (
        db.query(models.Maneuver)
        .where(models.Maneuver.entry_id == entry.id)
        .where(models.Maneuver.maneuver_type == "divert")
        .first()
    )
    final_datarate: models.Datarate = (
        db.query(models.Datarate)
        .where(models.Datarate.entry_id == entry.id)
        .order_by(models.Datarate.order.desc())
        .first()
    )
    final_time = final_datarate.time + entry.t_entry

    # Generate arc for probe trajectory
    height, lat, long = get_probe_arc(entry, maneuver, req.probe_ta_step)
    probe_lat_long = make_lat_long(height, lat, long)

    # Generate arc for carrier trajectory
    height, lat, long = get_carrier_arc(maneuver, req.carrier_ta_step, final_time)
    carrier_lat_long = make_lat_long(height, lat, long)

    return {"carrier": carrier_lat_long, "probe": probe_lat_long}


@router.post("/plot_entry")
def plot_trajectories():
    pass
