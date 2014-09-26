"""
Created on Tue Sep 23 16:54:34 2014

@author: Natural Solutions (Thomas)
"""

from sqlalchemy import (
   Boolean,
   Column,
   desc,
   DateTime,
   Float,
   ForeignKey,
   Index,
   Integer,
   Numeric,
   Sequence,
   String,
   text,
   UniqueConstraint
 )

from ecorelevesensor.models import Base, dbConfig

dialect = dbConfig['dialect']

class DataGsm(Base):
    __tablename__ = 'T_DataGsm'
    id = Column('PK_id', Integer, Sequence('seq_Tdatagsm_id'), primary_key=True)
    platform_ = Column(Integer, nullable=False)
    date_ = Column(DateTime, nullable=False)
    lat = Column(Numeric(9, 5), nullable=False)
    lon = Column(Numeric(9, 5), nullable=False)
    ele = Column(Integer)
    speed = Column(Integer)
    course = Column(Integer)
    hdop = Column(Float)
    vdop = Column(Float)
    sat_count = Column(Integer)
    checked = Column(Boolean, nullable=False, server_default='0')
    imported = Column(Boolean, nullable=False, server_default='0')
    if dialect == 'mssql':
        __table_args__ = (
            Index('idx_Tdatagsm_platform_checked_with_date_lat_lon_ele', platform_, checked, desc(date_), mssql_include=[lat, lon, ele]),
            UniqueConstraint(platform_, date_)
        )
    else:
        __table_args__ = (
            Index('idx_Tdatagsm_fkgsm_checked', platform_, checked),
            UniqueConstraint(platform_, date_)
        )