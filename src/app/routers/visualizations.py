from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import dependencies as deps
from app import schemas
from sql import crud, models

router = APIRouter(
    prefix="/visualizations",
    tags=["visualizations"],
)


@router.post(
    "/trajectory_selection/{target_body_id}",
    response_model=list[schemas.TrajectorySummary],
)
def trajectory_selection(
    target_body_id: int, req: schemas.TrajectoryRequest, db: Session = Depends(deps.get_db)
):
    result = crud.get_body_trajectories(db, target_body_id, filters=req.filters, limit=req.limit)
    print(result)
    return result
