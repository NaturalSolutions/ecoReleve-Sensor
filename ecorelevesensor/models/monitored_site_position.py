"""
Created on Mon Sep  1 14:38:09 2014

@author: Natural Solutions (Thomas)
"""

from sqlalchemy import (
    Column,
    DateTime,
    desc,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    Sequence,
    String
)

from ..models import Base, dbConfig
from .monitored_site import MonitoredSite

dialect = dbConfig['dialect']

# TODO: homogénéiser les notations à la fin d'eRelevé
class MonitoredSitePosition(Base):
    __tablename__ = 'TMonitoredStations_Positions'
    id = Column('TGeoPos_PK_ID', Integer, Sequence('seq_monitoredsiteposition_pk_id'),
                primary_key=True)
    #creator = Column('FK_creator', Integer)
    site = Column('TGeoPos_FK_TGeo_ID', Integer, ForeignKey(MonitoredSite.id), nullable=False)
    lat = Column('TGeoPos_LAT', Numeric(9,5,asdecimal=False), nullable=False)
    lon = Column('TGeoPos_LON', Numeric(9,5,asdecimal=False), nullable=False)
    ele = Column('TGeoPos_ELE', Float)
    precision = Column('TGeoPos_Precision', Integer)
    date = Column('TGeoPos_Date', DateTime)
    begin_date = Column('TGeoPos_Begin_Date', DateTime, nullable=False)
    end_date = Column('TGeoPos_End_Date', DateTime)
    comments = Column('TGeoPos_Comments', String)
    
    __table_args__ = (
        Index('idx_Tmonitoredsiteposition_site_begin', site, desc(begin_date)), 
    )
    
    def __json__(self, request):
        return{
            'lat':self.lat,
            'lon':self.lon,
            'begin':str(self.begin_date),
            'end':None if self.end_date is None else str(self.end_date)
        }