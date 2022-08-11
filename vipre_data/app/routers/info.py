from fastapi import APIRouter

from vipre_data.app import schemas
from vipre_data.sql.models import Entry, Trajectory, get_column_names

router = APIRouter(
    tags=["info"],
)


@router.get("/filters", response_model=schemas.response.FiltersResponse)
def get_filters():
    return {
        "TrajectoryFilters": get_trajectory_filters(),
        "EntryFilters": get_entry_filters(),
    }


@router.get("/filters/trajectories", response_model=list[schemas.utils.Filter])
def get_trajectory_filters():
    return schemas.utils.TrajectoryFilters


@router.get("/filters/entries", response_model=list[schemas.utils.Filter])
def get_entry_filters():
    return schemas.utils.EntryFilters


@router.get("/fields", response_model=schemas.response.FieldsResponse)
def get_fields():
    return {
        "TrajectoryFields": get_trajectory_fields(),
        "EntryFields": get_entry_fields(),
    }


@router.get("/fields/trajectories", response_model=list[str])
def get_trajectory_fields() -> list[str]:
    return list(schemas.response.Trajectory.__fields__)


@router.get("/fields/entries", response_model=list[str])
def get_entry_fields() -> list[str]:
    return list(schemas.response.Entry.__fields__)


@router.get("/version")
def version():
    return "v0.1.0"
