from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import dependencies as deps
from app import schemas
from sql import crud, models
from computations.conic_2point import conic_2point

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
    print(result)
    return result


@router.post("/get_entry_arc/{entry_id}", response_model=list[schemas.utils.LatLong])
def get_trajectory_arc(entry_id: int, db: Session = Depends(deps.get_db)):
    entry = db.query(models.Entry).where(models.Entry.id == entry_id).first()

    # conic_2point(
    #     r_1=,
    #     v_1=,
    #     t_1=,
    # )
    # TODO: implement
    pass


@router.post("/plot_entry")
def plot_trajectories():
    pass
