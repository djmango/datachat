from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Establish a connection to the database
scraping_url = f'mysql+pymysql://{os.getenv("SCRAPING_DATABASE_USER")}:{os.getenv("SCRAPING_DATABASE_PASS")}@{os.getenv("SCRAPING_DATABASE_URI")}'
scraping_engine = create_engine(scraping_url)
postgres_url = f'postgresql+psycopg2://{os.getenv("POSTGRES_DATABASE_USER")}:{os.getenv("POSTGRES_DATABASE_PASS")}@{os.getenv("POSTGRES_DATABASE_URI")}'
postgres_engine = create_engine(postgres_url)

# Set up the Session class
scraping_session = sessionmaker(bind=scraping_engine)
postgres_session = sessionmaker(bind=postgres_engine)


def get_db_scraping():
    db = scraping_session()
    try:
        yield db
    finally:
        db.close()

def get_db_postgres():
    db = postgres_session()
    try:
        yield db
    finally:
        db.close()
