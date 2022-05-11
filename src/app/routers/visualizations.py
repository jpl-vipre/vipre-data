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
def trajectory_selection(target_body_id: int, req: schemas.TrajectoryRequest):
    pass
