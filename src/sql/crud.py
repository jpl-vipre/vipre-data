from typing import Optional, Union

from sqlalchemy.orm import Query, Session

from app import schemas
from sql import models

filter_fields_map: dict[str, set] = {
    "Trajectory": schemas.trajectory_filter_fields,
    "Entry": schemas.entry_filter_fields,
}


def make_query(
    db: Session,
    model: Union[models.Trajectory, models.Entry],
    filters: schemas.Filters,
    fields: Optional[list[str]] = None,
    limit: Optional[int] = None,
) -> Query:
    query: Query = db.query(model)  # Initialize base query
    if fields:
        # Limit select to user-specified fields that are valid model attributes
        columns = [getattr(model, field, None) for field in fields]
        columns = list(filter(None, columns))  # Filter out invalid fields
        # Default to only returning ID's if no valid fields are passed
        query = query.with_only_columns(columns or model.id)
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
        if f.category == schemas.FilterCategory.SLIDER:
            f: schemas.FilterRangeRequest
            query = query.where(col >= f.lower)
            query = query.where(col <= f.upper)
        elif f.category == schemas.FilterCategory.CHECKBOX:
            f: schemas.FilterCheckboxRequest
            query = query.where(col == f.checked)
        elif f.category == schemas.FilterCategory.VALUE:
            f: schemas.FilterValueRequest
            query = query.where(col == f.value)
    # TODO: Is limiting rows going to be a problem? Do we need paging?
    if limit:
        query = query.limit(limit)  # Limit number of rows returned
    print(str(query))
    return query


# def query_trajectories(
#         db: Session,
#         filters: schemas.Filters, fields: Optional[list[str]] = None,
#         limit: Optional[int] = None
# ) -> Query:
#     return make_query(db, models.Trajectory, filters, fields, limit)
#
#
# def query_entries(
#         db: Session,
#         filters: schemas.Filters, fields: Optional[list[str]] = None,
#         limit: Optional[int] = None
# ) -> Query:
#     return make_query(db, models.Entry, filters, fields, limit)
