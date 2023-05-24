from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Amazon(Base):
    __tablename__ = "amazon"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    title = Column(String(500))  # assuming the text won't be longer than 500 characters
    link = Column(String(500))  # assuming the URL won't be longer than 500 characters
    image = Column(String(500))  # assuming the URL won't be longer than 500 characters
    price = Column(String(100))  # assuming price is a float
    stars = Column(Float)  # assuming stars is a float
    prime = Column(String(100))  # assuming the text won't be longer than 100 characters
    raters = Column(Integer)  # number of raters
