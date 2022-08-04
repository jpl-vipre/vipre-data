import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from vipre_data.app import dependencies as deps
from vipre_data.app import schemas
from vipre_data.app.schemas.utils import get_xyz_tuple, make_lat_lon
from vipre_data.computations.cart2sph import cart2sph
from vipre_data.sql import crud, models
from vipre_data.computations.conic_2point import conic_2point

router = APIRouter(
    prefix="/visualizations",
    tags=["visualizations"],
)


@router.post(
    "/trajectory_selection/{target_body_id}",
    response_model=list[schemas.response.TrajectorySummary],
)
def trajectory_selection(
    target_body_id: int, req: schemas.request.TrajectoryRequest, db: Session = Depends(deps.get_db)
):
    result = crud.get_body_trajectories(db, target_body_id, filters=req.filters, limit=req.limit)
    return result


@router.post("/get_entry_arc/{entry_id}", response_model=list[schemas.utils.LatLongH])
def get_trajectory_arc(
    entry_id: int, req: schemas.request.EntryArcRequest, db: Session = Depends(deps.get_db)
):
    entry: models.Entry = db.query(models.Entry).where(models.Entry.id == entry_id).first()
    maneuver: models.Maneuver = (
        db.query(models.Maneuver)
        .where(models.Maneuver.entry_id == entry.id)
        .where(models.Maneuver.maneuver_type == "divert")
        .first()
    )
    params = dict(
        r_1=get_xyz_tuple(maneuver, "pos_man"),
        r_2=get_xyz_tuple(entry, "pos_entry"),
        v_1=get_xyz_tuple(maneuver, "vel_man"),
        v_2=get_xyz_tuple(entry, "vel_entry"),
        t_1=np.array([[entry.trajectory.t_arr]]),
        # t_1=np.array([[maneuver.time_man]]),
        t_2=np.array([[entry.t_entry]]),
        mu=entry.target_body.mu,
        ta_step=req.ta_step,  # Just needs to be high enough for a smooth arc
        rev_check=0,  # Likely not ever changed by user
        time_flag=0,  # Likely not ever changed by user
    )
    pos_set, vel_set, time_set = conic_2point(**params)
    height, lat, lon = cart2sph(*pos_set)
    return make_lat_lon(height, lat, lon)


@router.post("/plot_entry")
def plot_trajectories():
    pass
