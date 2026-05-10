from sqlalchemy import Column, BigInteger, String, Boolean, Text
from app.database import Base

class Species(Base):
    __tablename__ = 'species'

    id = Column(BigInteger, primary_key=True, index=True)
    species_code = Column(String(50), unique=True, index=True)
    chinese_name = Column(String(100))
    scientific_name = Column(String(255))
    family = Column(String(100))
    genus = Column(String(100))
    common_group = Column(String(100))
    is_native = Column(Boolean)
    notes = Column(Text)
