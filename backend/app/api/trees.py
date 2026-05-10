from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tree import Tree

router = APIRouter(prefix='/trees', tags=['trees'])

class TreeCreate(BaseModel):
    plot_id: int
    inventory_cycle: Optional[str] = None
    tree_no: Optional[str] = None
    tree_status: Optional[str] = None
    record_type: Optional[str] = None
    line_distance_m: Optional[float] = None
    plot_tree_distance_m: Optional[float] = None
    species_code: Optional[str] = None
    species_name: Optional[str] = None
    dbh_cm: Optional[float] = None
    height_m: Optional[float] = None
    clear_bole_height_m: Optional[float] = None
    crown_class: Optional[str] = None
    estimated_volume_m3: Optional[float] = None
    volume_model_id: Optional[int] = None
    height_model_id: Optional[int] = None
    notes: Optional[str] = None

class TreeResponse(TreeCreate):
    id: int
    class Config:
        from_attributes = True

@router.get('/', response_model=List[TreeResponse])
def list_trees(db: Session = Depends(get_db)):
    return db.query(Tree).order_by(Tree.id).all()

@router.get('/{tree_id}', response_model=TreeResponse)
def get_tree(tree_id: int, db: Session = Depends(get_db)):
    item = db.query(Tree).filter(Tree.id == tree_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Tree not found')
    return item

@router.post('/', response_model=TreeResponse)
def create_tree(payload: TreeCreate, db: Session = Depends(get_db)):
    item = Tree(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
