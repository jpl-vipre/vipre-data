from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import dependencies as deps
from app import schemas
from sql import crud, models

router = APIRouter(
    prefix="/entries",
    tags=["entries"],
)


@router.post("/", response_model=list[schemas.response.Entry], response_model_exclude_unset=False)
def query_entries(req: schemas.request.EntryRequest, db: Session = Depends(deps.get_db)):
    query = crud.make_query(db, models.Entry, req.filters, req.fields, req.limit)
    result = query.all()
    print(result)
    return result


# @router.post(
#     "/{trajectory_id}",
#     response_model=list[schemas.Entry],
#     response_model_exclude_unset=False,
# )
# def query_trajectory_entries(
#     trajectory_id: int, req: schemas.EntryRequest, db: Session = Depends(deps.get_db)
# ):
#     query = crud.query_entries(db, req.filters, req.fields, req.limit, trajectory_id)
#     result = query.all()
#     print(result)
#     return result


@router.get("/{entry_id}", response_model=schemas.response.Entry)
def get_entry(entry_id: int, db: Session = Depends(deps.get_db)):
    result = crud.get_entry(db, entry_id)
    print(result)
    return result
