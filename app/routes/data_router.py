from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.pydantic_models import pydantic_models, PydanticModelName

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/{model_name}")
async def get_data(
    model_name: PydanticModelName,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    General database query endpoint.
    ...
    """

    # Get the corresponding DB model and Pydantic model
    db_model = pydantic_models[model_name]._db
    pydantic_model = pydantic_models[model_name]

    results = db.query(db_model).offset(skip).limit(limit).all()

    if not results:
        raise HTTPException(status_code=404, detail=f"{model_name.value} entries not found.")

    # Convert to Pydantic models
    results = [pydantic_model.from_orm(result) for result in results]
    return results
