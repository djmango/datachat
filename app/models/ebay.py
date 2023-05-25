from sqlalchemy import Column, Integer, String, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

Base = declarative_base()


class Ebay(Base):
    __tablename__ = "ebay"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    title = Column(String(500)) 
    link = Column(String(500))  
    image = Column(String(500)) 
    price = Column(String(100))  
    discount = Column(String(100))

class EbayBase(BaseModel):
    # https://docs.pydantic.dev/latest/usage/models/
    id : Optional[int] = Field(None, description="The id index")
    created_at : Optional[datetime] = Field(None, description="The date the entry was created")
    title : Optional[str] = Field(None, description="The title of the ebay product")
    link : Optional[str] = Field(None, description="The url to the ebay product")
    image : Optional[str] = Field(None, description="The link to the image")
    price : Optional[str] = Field(None, description="The price of the product")
    discount : Optional[str] = Field(None, description="The dicount on the product")
    _db = Ebay
    _datatype = "text"