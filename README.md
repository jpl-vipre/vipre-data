# VIPRE Data

This project will handle data management for the VIPRE Application, including data models, ingestion
scripts, and any
ad-hoc processing/exploration that needs to be performed.

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

This project uses `poetry` for dependency and environment management. See
the [Poetry Introduction docs](https://python-poetry.org/docs/) to learn more.

To get started run:

```shell
poetry install
```

Once your environment has been initialized with the proper packages, you can bring up the API REST
server with:

```shell
cd src/
poetry run uvicorn --reload --log-level debug app.main:app
```

## Building for Distribution

This project uses two separate build tools for generating the distribution files for unix and
Windows systems. First, `pex` was explored for generating a standalone executable file. This is a
single file which can be passed around and run independently of location/path on system. It was
later discovered that pex cannot build Windows exe files and thus a new tool was also
incorporated: `pyinstaller`. Even so, the Windows executable still must be built **on a Windows
device** which is currently done manually via VirtualBox.

### Building with Pex

[See the Docs](https://pex.readthedocs.io/en/v2.1.102/buildingpex.html)

Pex must be installed in the active environment (it is already included in the pyproject.toml). The
build command specifies a requirements.txt file for dependency installation, a working directory for
bundling source code, and a command that is used for starting the process when invoked. This can all
be done with the following command:

```shell
poetry run pex -r ../requirements.txt -D . -c uvicorn -o ../vipre-api.pex
```

To verify that the application was built successfully, run:

```shell
mv ../vipre-api.pex ~/Downloads
~/Downloads/vipre-api.pex app.main:app
```

<details>
<summary>PyInstaller on Mac</summary>
NOTE: I would like to build with PyInstaller on Mac as well, but have been unable to as of yet. PyInstaller fails due to a missing Python Library errors:

```console
OSError: Python library not found: Python3, libpython3.9.dylib, libpython3.9m.dylib, Python, .Python
    This means your Python installation does not come with proper shared library files.
    This usually happens due to missing development package, or unsuitable build parameters of the Python installation.

    * On Debian/Ubuntu, you need to install Python development packages:
      * apt-get install python3-dev
      * apt-get install python-dev
    * If you are building Python by yourself, rebuild with `--enable-shared` (or, `--enable-framework` on macOS).
```

When I follow this advice and try to rebuild python with `--enable-framework`, I get the following errors:

```console
$ env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.9.1
pyenv: /Users/mfedell/.pyenv/versions/3.9.1 already exists
continue with installation? (y/N) y
python-build: use openssl@1.1 from homebrew
python-build: use readline from homebrew
Downloading Python-3.9.1.tar.xz...
-> https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tar.xz
Installing Python-3.9.1...
python-build: use readline from homebrew
python-build: use zlib from xcode sdk

BUILD FAILED (OS X 12.4 using python-build 20180424)

Inspect or clean up the working tree at /var/folders/wv/gltyfn4j6f910j0cydhb2bwc0000gp/T/python-build.20220809182029.52630
Results logged to /var/folders/wv/gltyfn4j6f910j0cydhb2bwc0000gp/T/python-build.20220809182029.52630.log

Last 10 log lines:
checking for --with-cxx-main=<compiler>... no
checking for clang++... no
configure:

  By default, distutils will build C++ extension modules with "clang++".
  If this is not intended, then set CXX on the configure command line.

checking for the platform triplet based on compiler characteristics... darwin
configure: error: internal configure error for the platform triplet, please file a bug report
make: *** No targets specified and no makefile found.  Stop.
```

</details>

### Building with PyInstaller

[See the Docs](https://pyinstaller.org/en/stable/usage.html)

PyInstaller also must be installed in the active environment (it is already included in the
pyproject.toml). The build command relies on a spec file which was first generated by PyInstaller
and then modified after. Once this spec file is generated and present (it is version controlled with
this repo), builds can be rolled out quite simply.

> Note, the following commands assume an active environment. These are typically run on the Windows
> builder where poetry has been swapped out for a simpler python-venv based environment (python -m
> venv venv)

To generate the server.spec file that controls subsequent builds, run:

```shell
pyinstaller server.py --collect-all vipre_data
```

To create a new build, run:

```shell
pyinstaller server.spec -y
```

This will by default create a `dist/server/` folder with all the libraries and dependencies needed to run `dist/server/server.exe`. This entire folder can be zipped and distributed for local execution.

<details>
  <summary>Detailed Windows build instructions</summary>  
Execute the following from Git-Bash on VirtualBox:

```shell
cd Documents/vipre-data
git pull
python -m venv ./venv
. venv/Scripts/activate
# make sure that uvloop is not included in the requirements.txt file
pip install -r requirements.txt
pip install pyinstaller
pip install -e .
cd vipre_data
pyinstaller -y server.spec
```
</details>




## Interacting with the Database

The database is managed by a collection of tools. The schemas are defined in `vipre-schemas` which
are used to write
the `sqlalchemy` ORM models. These models are in turn read by the `alembic` migration tool which
creates migrations
in `alembic/versions/` to reflect the changes to those models. `alembic` is also used to connect to
the database and
execute those migrations when appropriate.

Interaction with the database relies on an initialized and active python environment

```shell
poetry install
poetry shell
```

For more information on these tools see the following docs:

- [SQLAlchemy Models](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [SQLAlchemy Database Connections](https://docs.sqlalchemy.org/en/14/core/engines.html)
- [Sqlite3](https://www.sqlite.org/quickstart.html)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/front.html)

Currently, the MatLab process (`vipre-gen`) performs all writes to the database and thus frequently
needs to create the
database as well. This is easily done by exporting a sql init script. This can be done directly with
alembic by
running `alembic upgrade head --sql` for an initial migration, or by connecting to the database
with `sqlite` and
running `.schema`. Examples are shown below.

> **NOTE**: be sure to check the autogenerated revision file before executing the `upgrade` command

Dump the current database schema (whatever is in `database.db`)

```shell
alembic revision --autogenerate "[revision message]"
alembic upgrade head
sqlite3 database.db ".schema" > init-db.sql
```

Use alembic to generate an initial schema and a corresponding init-db.sql file

```shell
alembic revision --autogenerate "Generate schema"
alembic upgrade head --sql > init-db.sql
```

Use alembic to generate a migration, upgrade the current database, and output the schema to an
init-db.sql file

```shell
alembic revision --autogenerate "[revision message]"
alembic upgrade head
sqlite3 database.db ".schema" > init-db.sql
```

**NOTE**: Since sqlite is being used at this phase, migrations are not all that important and it is
sometimes easier to
wipe the database and revision history to start from scratch. This can be done with the following:

```shell
cd src
rm -rf alembic/versions/*
rm -f database.db
alembic revision --autogenerate "Generate schema"
alembic upgrade head --sql > init-db.sql
```

