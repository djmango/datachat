from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Establish a connection to the database
url = f'mysql+pymysql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASS")}@{os.getenv("DATABASE_URI")}/scraping'
engine = create_engine(url)

# Set up the Session class
Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

