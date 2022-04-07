from fastapi import FastAPI

from sql.models import Entry, Trajectory, get_column_names
from app.routers import trajectories, info
from app import schemas

app = FastAPI()

app.include_router(trajectories.router)
app.include_router(info.router)


@app.get("/")
def get_root():
    return "Welcome to the VIPRE Data Service API"


@app.get("/version")
def version():
    return "v0.1.0"
