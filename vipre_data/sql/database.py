from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os

this_file = Path(__file__).absolute()
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
sample = f'sqlite:///{(this_file.parent / "E_S_test_big.db").absolute()}'
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", sample)

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
print(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
