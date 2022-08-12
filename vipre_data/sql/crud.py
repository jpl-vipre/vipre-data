from typing import Optional, Union, Type

from sqlalchemy.orm import Query, Session, defer

from vipre_data.app import schemas
from vipre_data.sql import models

filter_fields_map: dict[str, set] = {
    "Trajectory": schemas.utils.trajectory_filter_fields,
    "Entry": schemas.utils.entry_filter_fields,
}


def make_query(
    db: Session,
    model: Union[Type[models.Trajectory], Type[models.Entry]],
    filters: schemas.request.Filters,
    fields: Optional[list[str]] = None,
    limit: Optional[int] = None,
) -> Query:
    query: Query = db.query(model)  # Initialize base query
    # if fields:
    #     # Limit select to user-specified fields that are valid model attributes
    #     columns = [getattr(model, field, None) for field in fields]
    #     columns = list(filter(None, columns))  # Filter out invalid fields
    #     # Default to only returning ID's if no valid fields are passed
    #     query = query.with_only_columns(columns or model.id)
    for f in filters:
        # Ensure that all requested filter field_names are valid
        filter_fields = filter_fields_map.get(model.__name__, set())
        if f.field_name not in filter_fields:
            # TODO: should probably emit an error or at least a warning here
            print("INVALID FIELD_NAME; SKIPPING FILTER ", f.field_name)
            continue

        # Need to fetch the ORM column dynamically based on string field_name
        col = getattr(model, f.field_name)

        # Apply the appropriate where clause based on the filter type
        if f.category == schemas.utils.FilterCategory.SLIDER:
            f: schemas.request.FilterRangeRequest
            query = query.where(col >= f.lower)
            query = query.where(col <= f.upper)
        elif f.category == schemas.utils.FilterCategory.CHECKBOX:
            f: schemas.request.FilterCheckboxRequest
            query = query.where(col == f.checked)
        elif f.category == schemas.utils.FilterCategory.VALUE:
            f: schemas.request.FilterValueRequest
            query = query.where(col == f.value)
    # TODO: Is limiting rows going to be a problem? Do we need paging?
    if limit:
        query = query.limit(limit)  # Limit number of rows returned
    print(str(query))
    return query


def get_trajectory(db: Session, trajectory_id: int) -> models.Trajectory:
    return db.query(models.Trajectory).where(models.Trajectory.id == trajectory_id).first()


def get_trajectory_entries(
    db: Session, trajectory_id: int, limit: int, offset: int
) -> list[models.Entry]:
    query: Query = db.query(models.Entry).where(models.Entry.trajectory_id == trajectory_id)
    results = query.limit(limit).offset(offset).all()
    return results


def count_trajectory_entries(db: Session, trajectory_id: int) -> int:
    return db.query(models.Entry).where(models.Entry.trajectory_id == trajectory_id).count()


def get_entry(db: Session, entry_id: int) -> models.Trajectory:
    return db.query(models.Entry).where(models.Entry.id == entry_id).first()


def count_body_trajectories(db: Session, target_body_id) -> int:
    return db.query(models.Trajectory).where(models.Trajectory.body_id == target_body_id).count()


def get_body_trajectories(
    db: Session,
    target_body_id: int,
    filters: schemas.request.Filters,
    limit: Optional[int] = None,
) -> list[models.Trajectory]:
    query = db.query(models.Trajectory)
    query = query.where(models.Trajectory.body_id == target_body_id)
    return query.all()


def get_bodies(db: Session, body_id: Optional[int] = None) -> list[models.Body]:
    query = db.query(models.Body)
    if body_id:
        query = query.where(models.Body.id == body_id)
    return query.all()


# def query_trajectories(
#         db: Session,
#         filters: schemas.Filters, fields: Optional[list[str]] = None,
#         limit: Optional[int] = None
# ) -> Query:
#     return make_query(db, models.Trajectory, filters, fields, limit)
#
#
# def query_entries(
#     db: Session,
#     filters: schemas.Filters,
#     fields: Optional[list[str]] = None,
#     limit: Optional[int] = None,
#     trajectory_id: Optional[int] = None,
# ) -> Query:
#     filters.append(schemas.FilterValueRequest(field_name="trajectory_id", value=trajectory_id))
#     return make_query(db, models.Entry, filters, fields, limit)
