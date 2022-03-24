from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql import models, schema
from sql.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/version")
def version():
    return "v0.1.0"
