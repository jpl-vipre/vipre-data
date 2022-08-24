import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from vipre_data.app import dependencies as deps
from vipre_data.app import schemas
from vipre_data.app.schemas.utils import get_xyz_tuple, make_lat_long
from vipre_data.computations.cart2sph import cart2sph
from vipre_data.sql import crud, models
from vipre_data.computations.conic_2point import conic_2point
from vipre_data.computations.conic_1point import conic_1point

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


def get_carrier_arc(maneuver: models.Maneuver, final_time: int):
    # TODO: Implement via conic_1point
    params = dict(
        r_1=get_xyz_tuple(maneuver, "pos_man"),
        v_1=get_xyz_tuple(maneuver, "vel_man"),
        t_1=np.array([[maneuver.time_man]]),
        mu=maneuver.entry.target_body.mu,
        time_flag=0,  # Likely not ever changed by user
    )
    pos_set, vel_set, time_set = conic_1point(**params)
    # pos_set: [ [[ x1, x2 ]], [[ y1, y2 ]], [[ z1, z2 ]] ]
    # vel_set: same...
    # time_set: [ [[ t1, t2 ]] ]

    # Identify last valid entry in time_set (all tuples up to final_time)
    final_idx = 0
    for i, time in enumerate(time_set.flatten()):
        if time >= final_time:
            final_idx = i
            break

    #
    pos_set = pos_set[:, :, :final_idx]  # slice each component (x,y,z) up to final_idx
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

    # Generate arc for probe trajectory
    height, lat, long = get_probe_arc(entry, maneuver, req.ta_step)
    probe_lat_long = make_lat_long(height, lat, long)

    # Generate arc for carrier trajectory
    height, lat, long = get_carrier_arc(entry, final_datarate.time)
    carrier_lat_long = make_lat_long(height, lat, long)

    return {"carrier": carrier_lat_long, "probe": probe_lat_long}


@router.post("/plot_entry")
def plot_trajectories():
    pass
