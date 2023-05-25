from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.cnn import CnnBase as Cnn, Cnn as CnnModel
from app.db import get_db_text


# Assuming you have already defined get_db

router = APIRouter( responses={404: {"description": "Not found"}})

@router.get("/cnn", response_model=List[Cnn])
async def read_cnns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_text)):
    """ 
    Retrieve CNN entries.
    
    ## Path Parameters
    - `skip`: Number of entries to skip for the returned values (Default is 0)
    - `limit`: Maximum number of entries to return (Default is 100)
    
    ## Responses
    - `200`: Successful response. A list of CNN entries is returned.
    - `404`: CNN entry not found.
    """
    cnns = db.query(CnnModel).offset(skip).limit(limit).all()
    if cnns is None:
        raise HTTPException(status_code=404, detail="CNN entries not found")

    # Convert to CnnBase
    cnns = [Cnn.from_orm(cnn) for cnn in cnns]
    return cnns
