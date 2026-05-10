from sqlalchemy import Column, BigInteger, String, Integer, Numeric, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base

class VolumeModel(Base):
    __tablename__ = 'volume_models'

    id = Column(BigInteger, primary_key=True, index=True)
    species_code = Column(String(50), index=True)
    species_name = Column(String(100))
    model_name = Column(String(150))
    formula_text = Column(Text, nullable=False)
    formula_expression = Column(Text)
    variables = Column(JSONB)
    coefficients = Column(JSONB)
    applicable_region = Column(String(150))
    sample_size = Column(Integer)
    r_squared = Column(Numeric)
    author = Column(String(150))
    publication_year = Column(Integer)
    source_reference = Column(Text)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
