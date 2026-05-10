from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.species import Species

router = APIRouter(prefix='/species', tags=['species'])

class SpeciesCreate(BaseModel):
    species_code: str
    chinese_name: Optional[str] = None
    scientific_name: Optional[str] = None
    family: Optional[str] = None
    genus: Optional[str] = None
    common_group: Optional[str] = None
    is_native: Optional[bool] = None
    notes: Optional[str] = None

class SpeciesResponse(SpeciesCreate):
    id: int
    class Config:
        from_attributes = True

@router.get('/', response_model=List[SpeciesResponse])
def list_species(db: Session = Depends(get_db)):
    return db.query(Species).order_by(Species.id).all()

@router.get('/{species_id}', response_model=SpeciesResponse)
def get_species(species_id: int, db: Session = Depends(get_db)):
    item = db.query(Species).filter(Species.id == species_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Species not found')
    return item

@router.post('/', response_model=SpeciesResponse)
def create_species(payload: SpeciesCreate, db: Session = Depends(get_db)):
    item = Species(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
