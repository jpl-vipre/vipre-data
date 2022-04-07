from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import dependencies as deps
from app import schemas
from sql import crud

router = APIRouter(
    prefix="/trajectories",
    tags=["trajectories"],
)


@router.post("/", response_model=list[schemas.Trajectory])
def get_trajectories(req: schemas.DataRequest, db: Session = Depends(deps.get_db)):
    query = crud.query_trajectories(db, req.filters, req.fields, req.limit)
    return query.all()

