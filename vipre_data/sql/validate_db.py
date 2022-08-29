import logging

from sqlalchemy import inspect
from sqlalchemy.sql.schema import MetaData

logger = logging.getLogger(__name__)


def is_sane_database(Base, session):
    """Check whether the current database matches the models declared in model base.

    Currently we check that all tables exist with all columns. What is not checked

    * Column types are not verified

    * Relationships are not verified at all (TODO)

    :param Base: Declarative Base for SQLAlchemy models to check

    :param session: SQLAlchemy session bound to an engine

    :return: True if all declared models have corresponding tables and columns.
    """

    engine = session.get_bind()
    inspection = inspect(engine)
    db_tables: list[str] = inspection.get_table_names()

    base_mapper: MetaData = inspect(Base.metadata)

    errors = False

    # Go through all SQLAlchemy models
    for model in base_mapper.sorted_tables:

        table = model.name
        if table in db_tables:
            # Check all columns are found
            db_columns = {c["name"] for c in inspection.get_columns(table)}
            model_columns = {c.name for c in model.columns}
            if model_columns - db_columns:
                logger.error("Table %s is missing columns required by the data model", table)
                errors = True
        else:
            logger.error(
                "Model %s declares table %s which does not exist in database %s",
                model,
                table,
                engine.url.database,
            )
            errors = True

    return not errors
