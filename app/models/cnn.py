from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

Base = declarative_base()

class CnnBase(BaseModel):
    created_at: Optional[datetime] = Field(None, description="The creation datetime of the CNN entry.")
    category: Optional[str] = Field(None, description="The category of the CNN entry.")
    title: Optional[str] = Field(None, description="The title of the CNN entry.")
    link: Optional[str] = Field(None, description="The link of the CNN entry.")

class Cnn(Base):
    __tablename__ = "cnn"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    category = Column(String(500))  # assuming the URL won't be longer than 500 characters
    title = Column(String(500))  # assuming the text won't be longer than 500 characters
    link = Column(String(500))  # assuming the URL won't be longer than 500 characters
