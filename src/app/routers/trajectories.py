from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import dependencies as deps
from app import schemas
from sql import crud, models

router = APIRouter(
    prefix="/trajectories",
    tags=["trajectories"],
)


@router.post("/", response_model=list[schemas.Trajectory], response_model_exclude_unset=True)
def get_trajectories(req: schemas.TrajectoryRequest, db: Session = Depends(deps.get_db)):
    query = crud.make_query(db, models.Trajectory, req.filters, req.fields, req.limit)
    return query.all()
