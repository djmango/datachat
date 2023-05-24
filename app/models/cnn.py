from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cnn(Base):
    __tablename__ = "cnn"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    category = Column(String(500))  # assuming the URL won't be longer than 500 characters
    title = Column(String(500))  # assuming the text won't be longer than 500 characters
    link = Column(String(500))  # assuming the URL won't be longer than 500 characters
