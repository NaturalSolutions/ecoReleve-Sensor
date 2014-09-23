"""
Created on Tue Sep 23 16:54:34 2014

@author: Natural Solutions (Thomas)
"""

from sqlalchemy import (
   Boolean,
   Column,
   DateTime,
   Float,
   ForeignKey,
   Index,
   Integer,
   Numeric,
   Sequence,
   String
 )

from ecorelevesensor.models import Base, dbConfig
from .object import ObjectGsm

dialect = dbConfig['dialect']

class DataGsm(Base):
    __tablename__ = 'T_DataGsm'
    id = Column('PK_id', Integer, primary_key=True)
    gsm = Column('FK_gsm', Integer, ForeignKey(ObjectGsm.program_id), nullable=False)
    date_ = Column(DateTime, nullable=False)
    lat = Column(Numeric(9, 5), nullable=False)
    lon = Column(Numeric(9, 5), nullable=False)
    ele = Column(Integer)
    speed = Column(Integer)
    course = Column(Integer)
    hdop = Column(Float)
    vdop = Column(Float)
    checked = Column(Boolean, nullable=False, default=False)
    imported = Column(Boolean, nullable=False, default=False)
    #TODO: add dialect test for included column
    __table_args__ = (
        Index('idx_Tdatagsm_fkgsm_checked', gsm, checked),
    )