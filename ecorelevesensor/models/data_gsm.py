"""
Created on Tue Sep 23 16:54:34 2014

@author: Natural Solutions (Thomas)
"""

from sqlalchemy import (
   Boolean,
   Column,
   desc,
   DateTime,
   Index,
   Integer,
   Numeric,
   Sequence,
   UniqueConstraint
 )

from ecorelevesensor.models import Base, dbConfig

dialect = dbConfig['dialect']


#TODO: Foreign Key on platform_ referencing T_ObjectGsm.platform_
class DataGsm(Base):
    __tablename__ = 'T_DataGsm'
    id = Column('PK_id', Integer, Sequence('seq_Tdatagsm_id'), primary_key=True)
    platform_ = Column(Integer, nullable=False)
    date = Column('DateTime', DateTime, nullable=False)
    lat = Column('Latitude_N', Numeric(9, 5, asdecimal=False), nullable=False)
    lon = Column('Longitude_E', Numeric(9, 5, asdecimal=False), nullable=False)
    speed = Column('Speed', Integer)
    course = Column('Course', Integer)
    ele = Column('Altitude_m', Integer)
    hdop = Column('HDOP', Numeric(2, 1, asdecimal=False))
    vdop = Column('VDOP', Numeric(2, 1, asdecimal=False))
    sat_count = Column('SatelliteCount', Integer)
    checked = Column(Boolean, nullable=False, server_default='0')
    imported = Column(Boolean, nullable=False, server_default='0')
    if dialect == 'mssql':
        __table_args__ = (
            Index('idx_Tdatagsm_platform_checked_with_date_lat_lon_ele', platform_, checked, desc(date), mssql_include=[lat, lon, ele]),
            UniqueConstraint(platform_, date)
        )
    else:
        __table_args__ = (
            Index('idx_Tdatagsm_fkgsm_checked', platform_, checked),
            UniqueConstraint(platform_, date)
        )