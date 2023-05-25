from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Get environment variable values
db_uri = os.getenv('POSTGRES_DATABASE_URI')
db_user = os.getenv('POSTGRES_DATABASE_USER')
db_pass = os.getenv('POSTGRES_DATABASE_PASS')

engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_uri}")
Base = declarative_base()

df_meta = pd.read_sql("SELECT * FROM data_stream_metadata", engine)

def numeric_model(table_name):

    class Numeric(Base):
        __tablename__ = table_name

        created_at = Column(DateTime)
        category = Column(String(500))  # assuming the URL won't be longer than 500 characters
        title = Column(String(500))  # assuming the text won't be longer than 500 characters
        link = Column(String(500))  # assuming the URL won't be longer than 500 characters

    class NumericBase(BaseModel):
        # https://docs.pydantic.dev/latest/usage/models/
        created_at: Optional[datetime] = Field(None, description="The creation datetime of the entry.")
        id: Optional[str] = Field(None, description="The int id of the entry")
        title: Optional[str] = Field(None, description="The title of the CNN article.")
        link: Optional[str] = Field(None, description="The link of the CNN article.")
        class Config:
           orm_mode = True
        _db = Numeric
        _datatype = "text"
        class Config:
           orm_mode = True