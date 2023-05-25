from sqlalchemy import Column, Integer, String, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

Base = declarative_base()

class Yelp(Base):
    __tablename__ = "yelp"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    resturant_name = Column(String(500)) 
    link = Column(String(500))  
    image = Column(String(500)) 
    price_category = Column(String(500))  
    when_opened = Column(String(1000))
    resturant_overview = Column(String(3000))


class YelpBase(BaseModel):
    # https://docs.pydantic.dev/latest/usage/models/
    id : Optional[int] = Field(None, description="The id index")
    created_at : Optional[datetime] = Field(None, description="The date the entry was created")
    resturant_name : Optional[str] = Field(None, description="The name of the resturant")
    link : Optional[str] = Field(None, description="The link to the resturant website")
    image : Optional[str] = Field(None, description="The image of the resturant")
    price_category : Optional[str] = Field(None, description="The category of food and the price rage of the resturant")
    when_opened : Optional[str] = Field(None, description="The opening time of the resturant or the day that it opened")
    resturant_overview : Optional[str] = Field(None, description="The review of the resturant written by customers")
    _db = Yelp
    _datatype = "text"