# VIPRE Data

This project will handle data management for the VIPRE Application, including data models, ingestion scripts, and any ad-hoc processing/exploration that needs to be performed.

## Contents

```text
.
├── README.md                       This file
├── data/                           Collection of seed data for development and testing
├── docs/                           Documentation for the design and development of this application
│     ├── ERD.drawio                Entity Relationship Diagram capturing the data model's relationships
│     ├── ERD.png
│     ├── backend_service.md        Notes on the design of the backend data service
│     ├── draft_er.png              Archive
│     ├── example_tables.png        Example of some data tables in spreadsheet format
│     ├── old_data_dictionary.md    Archive
│     └── sample_table_data.xlsx    Example of some data tables in spreadsheet format
├── notebooks/                      Notebooks for ad-hoc processing or data exploration
├── pyproject.toml                  Configuration for the project - managed by `poetry`
├── schemas/                        Data schemas in static text files
│     ├── vipre_schema-*.csv        Exported from a shared google sheet where the data model was developed
│     └── vipre_schema-*.json       Converted from csvs to provide easily parsable schema to various consumers
├── scripts/
│     └── make_schemas.py           Converts the csv files found in schemas/ to the json format with metadata
├── src/                            Source code for the application
│     ├── alembic/                  Configuration and versions for database migrations - managed by `alembic` 
│     ├── alembic.ini               Configuration for the alembic tool
│     ├── app/                      FastAPI Python application
│     │     ├── dependencies.py     Global dependencies used across the API
│     │     ├── main.py             Main FastAPI application and top-level utility routes
│     │     ├── routers/            Collection of routers that service the primary application routes 
│     │     └── schemas.py          Schema objects that define request/response models
│     ├── database.db               SQLite database for development and testing
│     ├── init-db.sql               SQL schema export from the sqlalchemy/alembic managed database; kept for portability
│     └── sql/
│         ├── database.py           Manages database connections and utilities
│         └── models.py             Defines the data models using the sqlalchemy ORM 
```

## Running the Application

This project uses `poetry` for dependency and environment management. See the [Poetry Introduction docs](https://python-poetry.org/docs/) to learn more.

To get started run:

```shell
poetry install
```

Once your environment has been initialized with the proper packages, you can bring up the API REST server with:

```shell
cd src/
poetry run uvicorn --reload --log-level debug app.main:app
```
