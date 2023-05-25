from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.models.pydantic_models import pydantic_models
import os
from typing import AsyncGenerator

# Establish a connection to the database
scraping_url = f'mysql+pymysql://{os.getenv("SCRAPING_DATABASE_USER")}:{os.getenv("SCRAPING_DATABASE_PASS")}@{os.getenv("SCRAPING_DATABASE_URI")}'
scraping_engine = create_engine(scraping_url)
postgres_url = f'postgresql+psycopg2://{os.getenv("POSTGRES_DATABASE_USER")}:{os.getenv("POSTGRES_DATABASE_PASS")}@{os.getenv("POSTGRES_DATABASE_URI")}'
postgres_engine = create_engine(postgres_url)

# Set up the Session class
scraping_session = sessionmaker(bind=scraping_engine)
postgres_session = sessionmaker(bind=postgres_engine)


def get_db_text():
    db = scraping_session()
    try:
        yield db
    finally:
        db.close()

def get_db_numeric():
    db = postgres_session()
    try:
        yield db
    finally:
        db.close()

async def get_db(model_name: str) -> AsyncGenerator[Session, None]:
    datatype = pydantic_models[model_name]._datatype
    db = None
    try:
        if datatype == "numeric":
            db = get_db_numeric()
        elif datatype == "text":
            db = get_db_text()
        else:
            raise ValueError(f"Invalid datatype {datatype} for model {model_name}")
        yield next(db)
    finally:
        if db:
            db.close()
