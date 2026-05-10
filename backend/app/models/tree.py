from sqlalchemy import Column, BigInteger, String, Numeric, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Tree(Base):
    __tablename__ = 'trees'

    id = Column(BigInteger, primary_key=True, index=True)
    plot_id = Column(BigInteger, ForeignKey('plots.id', ondelete='CASCADE'), index=True)
    inventory_cycle = Column(String(20), index=True)
    tree_no = Column(String(50))
    tree_status = Column(String(50))
    record_type = Column(String(50))
    line_distance_m = Column(Numeric)
    plot_tree_distance_m = Column(Numeric)
    species_code = Column(String(50), index=True)
    species_name = Column(String(100))
    dbh_cm = Column(Numeric)
    height_m = Column(Numeric)
    clear_bole_height_m = Column(Numeric)
    crown_class = Column(String(50))
    estimated_volume_m3 = Column(Numeric)
    volume_model_id = Column(BigInteger, ForeignKey('volume_models.id'))
    height_model_id = Column(BigInteger, ForeignKey('height_models.id'))
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
