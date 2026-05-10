from sqlalchemy import Column, BigInteger, String, Numeric, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class Plot(Base):
    __tablename__ = "plots"

    id = Column(BigInteger, primary_key=True, index=True)
    plot_code = Column(String(100), index=True)
    inventory_cycle = Column(String(20), index=True)
    original_plot_id = Column(String(100))
    county = Column(String(100))
    township = Column(String(100))
    forest_district = Column(String(100))
    working_circle = Column(String(100))
    compartment = Column(String(100))
    sub_compartment = Column(String(100))
    elevation_m = Column(Numeric)
    slope_degree = Column(Numeric)
    aspect_degree = Column(Numeric)
    forest_type = Column(String(100))
    land_use_type = Column(String(100))
    plot_area_ha = Column(Numeric)
    x_coord = Column(Numeric)
    y_coord = Column(Numeric)
    longitude = Column(Numeric)
    latitude = Column(Numeric)
    source_file = Column(Text)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
