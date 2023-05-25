from sqlalchemy import Column, Integer, String, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

Base = declarative_base()

class Medium(Base):
    __tablename__ = "medium"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    title = Column(String(500)) 
    article_image_icon = Column(String(500))  
    writer_name = Column(String(500)) 
    writer_group = Column(String(500))  
    main_title = Column(String(1000))
    second_title_text = Column(String(1000))

class MediumBase(BaseModel):
    # https://docs.pydantic.dev/latest/usage/models/
    id : Optional[int] = Field(None, description="The id index")
    created_at : Optional[datetime] = Field(None, description="The date the entry was created")
    title : Optional[str] = Field(None, description="The title of the ebay product")
    article_image_icon : Optional[str] = Field(None, description="The link to the image")
    writer_name : Optional[str] = Field(None, description="The name of the author")
    writer_group : Optional[str] = Field(None, description="The company that the writer works for")
    main_title : Optional[str] = Field(None, description="The title of the article")
    second_title_text : Optional[str] = Field(None, description="A secondary title for the article")
    _db = Medium
    _datatype = "text"