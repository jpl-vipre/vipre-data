from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from vipre_data.app import dependencies as deps
from vipre_data.app import schemas
from vipre_data.sql import crud, models

router = APIRouter(
    prefix="/trajectories",
    tags=["trajectories"],
)


@router.post(
    "/", response_model=list[schemas.response.Trajectory], response_model_exclude_unset=True
)
def get_trajectories(req: schemas.request.TrajectoryRequest, db: Session = Depends(deps.get_db)):
    query = crud.make_query(db, models.Trajectory, req.filters, req.fields, req.limit)
    result = query.all()
    return result


@router.get("/{trajectory_id}", response_model=schemas.response.Trajectory)
def get_trajectory(trajectory_id: int, db: Session = Depends(deps.get_db)):
    result = crud.get_trajectory(db, trajectory_id)
    return result


@router.get("/{trajectory_id}/entries", response_model=list[schemas.response.Entry])
def get_trajectory_entries(
    trajectory_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(deps.get_db)
):
    result = crud.get_trajectory_entries(db, trajectory_id, limit, offset)
    # TODO: add LatLongH field to all the entries
    return result


@router.get("/{trajectory_id}/entries/count", response_model=int)
def count_trajectory_entries(trajectory_id: int, db: Session = Depends(deps.get_db)):
    result = crud.count_trajectory_entries(db, trajectory_id)
    return result
