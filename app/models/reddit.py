from sqlalchemy import Column, Integer, String, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

Base = declarative_base()



class Reddit(Base):
    __tablename__ = "reddit"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    subreddit = Column(String(500)) 
    advertiser_category = Column(String(500))  
    author = Column(String(500)) 
    total_karma = Column(Integer)  
    score = Column(Integer)
    title = Column(String(1000))
    ups = Column(Integer)
    upvote_ratio = Column(Float)
    selftext = Column(String(1000))
    thumbnail = Column(String(1000))
    domain = Column(String(1000))
    created = Column(Integer)


class RedditBase(BaseModel):
    # https://docs.pydantic.dev/latest/usage/models/
    id : Optional[int] = Field(None, description="The id index")
    created_at : Optional[datetime] = Field(None, description="The date the entry was created")
    subreddit : Optional[str] = Field(None, description="The subreddit or category that the post belongs to")
    advertiser_category : Optional[str] = Field(None, description="The category of the post for advertising use")
    author : Optional[str] = Field(None, description="The name of the author")
    total_karma : Optional[str] = Field(None, description="The total amount of reddit karma(points) that the post generated")
    score : Optional[str] = Field(None, description="The score of the post")
    title : Optional[str] = Field(None, description="The title of the reddit post")
    ups : Optional[str] = Field(None, description="The total amount of upvotes for the post")
    upvote_ratio : Optional[str] = Field(None, description="The upvote ratio of the post")
    selftext : Optional[str] = Field(None, description="The content of the post")
    thumbnail : Optional[str] = Field(None, description="The url to the thumbnail")
    domain : Optional[str] = Field(None, description="The domain of the post")
    created : Optional[str] = Field(None, description="The unix time creation of the post")
    _db = Reddit
    _datatype = "text"