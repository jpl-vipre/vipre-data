from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from vipre_data.app import dependencies as deps
from vipre_data.app import schemas
from vipre_data.sql import crud

router = APIRouter(
    prefix="/bodies",
    tags=["bodies"],
)


@router.get("/", response_model=list[schemas.response.Body])
def get_bodies(db: Session = Depends(deps.get_db)):
    return crud.get_bodies(db)


@router.get("/targeted", response_model=list[schemas.response.BodySummary])
def get_targeted_bodies(db: Session = Depends(deps.get_db)):
    """
    Retrieve the set of all targeted bodies in the database.

    Targeted bodies are those for which there exist some trajectories terminating at the body.
    There may be other bodies present in the sequence of flybys that are never present as the
    ultimate destination of a trajectory (e.g. not a target body)
    """
    return crud.get_targeted_bodies(db)


@router.get("/body/{body_id}", response_model=schemas.response.Body)
def get_body(body_id: int, db: Session = Depends(deps.get_db)):
    bodies = crud.get_bodies(db, body_id=body_id)
    if len(bodies) == 0:
        raise HTTPException(404, f"No body was found with the ID: {body_id}")
    return bodies[0]


@router.get("/list", response_model=list[schemas.response.BodySummary])
def list_bodies(db: Session = Depends(deps.get_db)):
    return crud.get_bodies(db)


@router.get("/architecture", response_model=list[schemas.response.BodySummary])
def get_architecture(architecture_sequence: str, db: Session = Depends(deps.get_db)):
    bodies = [
        crud.get_bodies(db, int(body_id.strip())) for body_id in architecture_sequence.split("-")
    ]
