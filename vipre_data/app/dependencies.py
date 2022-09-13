import os
from pathlib import Path

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session


# from vipre_data.sql.database import SessionLocal

# Dependency
def get_engine():
    this_file = Path(__file__).absolute()
    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
    sample = f'sqlite:///{(this_file.parent / "E_S_test_subset2.db").absolute()}'
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", sample)

    engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
    return engine


def get_db(engine: Engine = Depends(get_engine)):
    db = Session(autocommit=False, autoflush=False, bind=engine)
    try:
        yield db
    finally:
        db.close()
