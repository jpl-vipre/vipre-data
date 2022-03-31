from fastapi import FastAPI

from sql.models import Entry, Trajectory, get_column_names
from app.routers import trajectories
from app import schemas

app = FastAPI()

app.include_router(trajectories.router)


@app.get("/")
def get_root():
    return "Welcome to the VIPRE Data Service API"


@app.get("/version")
def version():
    return "v0.1.0"


@app.get("/filters", response_model=schemas.FiltersResponse)
def get_filters():
    return {
        "TrajectoryFilters": get_trajectory_filters(),
        "EntryFilters": get_entry_filters(),
    }


@app.get("/filters/trajectories", response_model=list[schemas.Filter])
def get_trajectory_filters():
    return schemas.TrajectoryFilters


@app.get("/filters/entries", response_model=list[schemas.Filter])
def get_entry_filters():
    return schemas.EntryFilters


@app.get("/fields", response_model=schemas.FieldsResponse)
def get_fields():
    return {
        "TrajectoryFields": get_trajectory_fields(),
        "EntryFields": get_entry_fields(),
    }


@app.get("/fields/trajectories", response_model=list[str])
def get_trajectory_fields() -> list[str]:
    return get_column_names(Trajectory)


@app.get("/fields/entries", response_model=list[str])
def get_entry_fields() -> list[str]:
    return get_column_names(Entry)
