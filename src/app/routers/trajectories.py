from fastapi import APIRouter
from sqlalchemy.sql import select, expression

from app import schemas
from sql import models

router = APIRouter(
    prefix="/trajectories",
    tags=["trajectories"],
)


@router.post("/")
def get_trajectories(req: schemas.TrajectoryRequest):
    query: expression.Select = select(models.Trajectory)  # Initialize base query
    if req.fields:
        columns = [getattr(models.Trajectory, field, None) for field in req.fields]
        columns = list(filter(None, columns))
        query = query.with_only_columns(columns or models.Trajectory.id)
    for f in req.filters:
        # Ensure that all requested filter field_names are valid
        if f.field_name not in schemas.trajectory_filter_fields:
            # TODO: should probably emit an error or at least a warning here
            continue

        # Need to fetch the ORM column dynamically based on string field_name
        col = getattr(models.Trajectory, f.field_name)

        # Apply the appropriate where clause based on the filter type
        if f.category == schemas.FilterCategory.RANGE:
            f: schemas.FilterRangeRequest
            query = query.where(col > f.lower)
            query = query.where(col < f.upper)
        elif f.category == schemas.FilterCategory.CHECKBOX:
            f: schemas.FilterCheckboxRequest
            query = query.where(col == f.checked)
        elif f.category == schemas.FilterCategory.VALUE:
            f: schemas.FilterValueRequest
            query = query.where(col == f.value)

    return str(query)