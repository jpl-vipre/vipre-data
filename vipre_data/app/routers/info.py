import os

from fastapi import APIRouter, Depends, Body
from fastapi import Request
from sqlalchemy import inspect
from sqlalchemy.engine import Engine, reflection
from sqlalchemy.orm import Session

from vipre_data.app import schemas
from vipre_data.app.dependencies import get_db, get_engine
from vipre_data.sql.models import VERSION as DATABASE_VERSION

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
def get_version(request: Request):
    return request.app.version


@router.get("/database", response_model=schemas.response.DbInfo)
def get_database_info(db: Session = Depends(get_db)):
    """Fetch information about the connected database"""
    engine: Engine = db.get_bind()
    return {
        "database": engine.url.database,
        "tables": engine.table_names(),
        "schema_version": DATABASE_VERSION,
    }


@router.get("/database/tables", response_model=list[str])
def get_database_tables(db: Session = Depends(get_db)) -> list[str]:
    """Fetch tables in the database"""
    engine: Engine = db.get_bind()
    return engine.table_names()


@router.get("/database/columns/{tablename}", response_model=list[str])
def get_table_columns(tablename: str, db: Session = Depends(get_db)) -> list[str]:
    """Fetch all column names in the database for a specified table"""
    engine: Engine = db.get_bind()
    inspection: reflection.Inspector = inspect(engine)
    columns = inspection.get_columns(tablename)
    return [c["name"] for c in columns]


@router.get("/database/connection")
def get_database_connection(engine: Engine = Depends(get_engine)):
    return engine.url.render_as_string()


@router.post("/database/connection")
def set_database_connection(uri: str = Body()):
    os.environ["SQLALCHEMY_DATABASE_URI"] = uri
    return uri
