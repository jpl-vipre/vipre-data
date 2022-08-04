from fastapi import FastAPI

from vipre_data.app.routers import trajectories, entries, info, visualizations, bodies

app = FastAPI()

app.include_router(visualizations.router)
app.include_router(trajectories.router)
app.include_router(entries.router)
app.include_router(bodies.router)
app.include_router(info.router)


@app.get("/")
def get_root():
    return "Welcome to the VIPRE Data Service API"
