from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.plot import Plot

router = APIRouter(prefix='/plots', tags=['plots'])


class PlotCreate(BaseModel):
    plot_code: str
    inventory_cycle: str
    original_plot_id: Optional[str] = None
    county: Optional[str] = None
    township: Optional[str] = None
    forest_district: Optional[str] = None
    working_circle: Optional[str] = None
    compartment: Optional[str] = None
    sub_compartment: Optional[str] = None
    elevation_m: Optional[float] = None
    slope_degree: Optional[float] = None
    aspect_degree: Optional[float] = None
    forest_type: Optional[str] = None
    land_use_type: Optional[str] = None
    plot_area_ha: Optional[float] = None
    x_coord: Optional[float] = None
    y_coord: Optional[float] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    source_file: Optional[str] = None
    notes: Optional[str] = None


class PlotResponse(PlotCreate):
    id: int

    class Config:
        from_attributes = True


@router.get('/', response_model=List[PlotResponse])
def list_plots(db: Session = Depends(get_db)):
    return db.query(Plot).order_by(Plot.id).all()


@router.get('/{plot_id}', response_model=PlotResponse)
def get_plot(plot_id: int, db: Session = Depends(get_db)):
    plot = db.query(Plot).filter(Plot.id == plot_id).first()
    if plot is None:
        raise HTTPException(status_code=404, detail='Plot not found')
    return plot


@router.post('/', response_model=PlotResponse)
def create_plot(payload: PlotCreate, db: Session = Depends(get_db)):
    plot = Plot(**payload.model_dump())
    db.add(plot)
    db.commit()
    db.refresh(plot)
    return plot
