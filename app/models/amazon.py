from sqlalchemy import Column, Integer, String, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

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

class AmazonBase(BaseModel):
    # https://docs.pydantic.dev/latest/usage/models/
    id : Optional[int] = Field(None, description="The id index")
    created_at : Optional[datetime] = Field(None, description="The date the entry was created")
    title : Optional[str] = Field(None, description="The title of the amazon product")
    link : Optional[str] = Field(None, description="The url to the amazon product")
    image : Optional[str] = Field(None, description="The link to the image")
    price : Optional[str] = Field(None, description="The price of the product")
    stars : Optional[float] = Field(None, description="The average number of stars on the product")
    prime : Optional[str] = Field(None, description="The amazon prime status of the product")
    raters : Optional[int] = Field(None, description="The number of people who rated the product")
    _db = Amazon
    _datatype = "text"

    class Config:
       orm_mode = True