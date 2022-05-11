from fastapi import FastAPI

from app.routers import trajectories, entries, info, visualizations

app = FastAPI()

app.include_router(trajectories.router)
app.include_router(entries.router)
app.include_router(info.router)
app.include_router(visualizations.router)


@app.get("/")
def get_root():
    return "Welcome to the VIPRE Data Service API"
