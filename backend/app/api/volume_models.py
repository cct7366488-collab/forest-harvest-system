from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.volume_model import VolumeModel

router = APIRouter(prefix='/volume-models', tags=['volume_models'])

class VolumeModelCreate(BaseModel):
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

class VolumeModelResponse(VolumeModelCreate):
    id: int
    class Config:
        from_attributes = True

@router.get('/', response_model=List[VolumeModelResponse])
def list_volume_models(db: Session = Depends(get_db)):
    return db.query(VolumeModel).order_by(VolumeModel.id).all()

@router.get('/{model_id}', response_model=VolumeModelResponse)
def get_volume_model(model_id: int, db: Session = Depends(get_db)):
    item = db.query(VolumeModel).filter(VolumeModel.id == model_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Volume model not found')
    return item

@router.post('/', response_model=VolumeModelResponse)
def create_volume_model(payload: VolumeModelCreate, db: Session = Depends(get_db)):
    item = VolumeModel(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
