from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import dependencies as deps
from app import schemas
from sql import crud, models

router = APIRouter(
    prefix="/bodies",
    tags=["bodies"],
)


@router.get("/", response_model=list[schemas.response.Body])
def get_bodies(db: Session = Depends(deps.get_db)):
    return crud.get_bodies(db)


@router.get("/body/{body_id}", response_model=schemas.response.Body)
def get_body(body_id: int, db: Session = Depends(deps.get_db)):
    bodies = crud.get_bodies(db, body_id=body_id)
    if len(bodies) == 0:
        raise HTTPException(404, f"No body was found with the ID: {body_id}")
    return bodies[0]


@router.get("/list", response_model=list[schemas.response.BodySummary])
def list_bodies(db: Session = Depends(deps.get_db)):
    return crud.get_bodies(db)
