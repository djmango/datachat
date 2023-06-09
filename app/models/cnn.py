from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

Base = declarative_base()

class Cnn(Base):
    __tablename__ = "cnn"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    category = Column(String(500))  # assuming the URL won't be longer than 500 characters
    title = Column(String(500))  # assuming the text won't be longer than 500 characters
    link = Column(String(500))  # assuming the URL won't be longer than 500 characters

class CnnBase(BaseModel):
    # https://docs.pydantic.dev/latest/usage/models/
    created_at: Optional[datetime] = Field(None, description="The creation datetime of the entry.")
    id: Optional[str] = Field(None, description="The int id of the entry")
    title: Optional[str] = Field(None, description="The title of the CNN article.")
    link: Optional[str] = Field(None, description="The link of the CNN article.")

    class Config:
       orm_mode = True

    _db = Cnn
    _datatype = "text"
