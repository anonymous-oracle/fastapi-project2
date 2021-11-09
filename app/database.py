from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

USERNAME = "postgres"
PASSWORD = "1234"
DBNAME = "fastapi"
HOSTNAME = "127.0.0.1"
PORT = 5432
SQLALCHEMY_DATABASE_URL = (
    f"""postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DBNAME}"""
)

engine_ = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

def get_db():
    db = Session(autocommit=False, autoflush=False, bind=engine_)
    try:
        yield db
    finally:
        db.close()