from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.height_model import HeightModel

router = APIRouter(prefix='/height-models', tags=['height_models'])

class HeightModelCreate(BaseModel):
    species_code: Optional[str] = None
    species_name: Optional[str] = None
    model_name: Optional[str] = None
    formula_text: str
    formula_expression: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None
    coefficients: Optional[Dict[str, Any]] = None
    applicable_region: Optional[str] = None
    sample_size: Optional[int] = None
    r_squared: Optional[float] = None
    author: Optional[str] = None
    publication_year: Optional[int] = None
    source_reference: Optional[str] = None
    notes: Optional[str] = None

class HeightModelResponse(HeightModelCreate):
    id: int
    class Config:
        from_attributes = True

@router.get('/', response_model=List[HeightModelResponse])
def list_height_models(db: Session = Depends(get_db)):
    return db.query(HeightModel).order_by(HeightModel.id).all()

@router.get('/{model_id}', response_model=HeightModelResponse)
def get_height_model(model_id: int, db: Session = Depends(get_db)):
    item = db.query(HeightModel).filter(HeightModel.id == model_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Height model not found')
    return item

@router.post('/', response_model=HeightModelResponse)
def create_height_model(payload: HeightModelCreate, db: Session = Depends(get_db)):
    item = HeightModel(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
