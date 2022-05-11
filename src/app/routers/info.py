from fastapi import APIRouter

from app import schemas
from sql.models import Entry, Trajectory, get_column_names

router = APIRouter(
    tags=["info"],
)


@router.get("/filters", response_model=schemas.FiltersResponse)
def get_filters():
    return {
        "TrajectoryFilters": get_trajectory_filters(),
        "EntryFilters": get_entry_filters(),
    }


@router.get("/filters/trajectories", response_model=list[schemas.Filter])
def get_trajectory_filters():
    return schemas.TrajectoryFilters


@router.get("/filters/entries", response_model=list[schemas.Filter])
def get_entry_filters():
    return schemas.EntryFilters


@router.get("/fields", response_model=schemas.FieldsResponse)
def get_fields():
    return {
        "TrajectoryFields": get_trajectory_fields(),
        "EntryFields": get_entry_fields(),
    }


@router.get("/fields/trajectories", response_model=list[str])
def get_trajectory_fields() -> list[str]:
    return get_column_names(Trajectory)


@router.get("/fields/entries", response_model=list[str])
def get_entry_fields() -> list[str]:
    return get_column_names(Entry)


@router.get("/version")
def version():
    return "v0.1.0"
