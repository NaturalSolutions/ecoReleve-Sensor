"""
Created on Mon Sep  1 14:38:09 2014

@author: Natural Solutions (Thomas)
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    desc,
    Float,
    ForeignKey,
    func,
    Index,
    Integer,
    Numeric,
    Sequence,
    String,
    UniqueConstraint
)

from ..models import Base, dbConfig
from .monitored_site import MonitoredSite

dialect = dbConfig['dialect']

# TODO: homogénéiser les notations à la fin d'eRelevé
class MonitoredSitePosition(Base):
    __tablename__ = 'TMonitoredStations_Positions'
    id = Column('TGeoPos_PK_ID', Integer, Sequence('seq_monitoredsiteposition_pk_id'),
                primary_key=True)
    creator = Column('FK_creator', Integer)
    site = Column('TGeoPos_FK_TGeo_ID', Integer, ForeignKey(MonitoredSite.id), nullable=False)
    lat = Column('TGeoPos_LAT', Numeric(9,5), nullable=False)
    lon = Column('TGeoPos_LON', Numeric(9,5), nullable=False)
    ele = Column('TGeoPos_ELE', Float)
    precision = Column('TGeoPos_Precision', Integer)
    date = Column('TGeoPos_Date', DateTime)
    begin_date = Column('TGeoPos_Begin_Date', DateTime)
    end_date = Column('TGeoPos_End_Date', DateTime)
    comments = Column('TGeoPos_Comments', String)
    
    __table_args__ = (
        Index('idx_Tmonitoredsiteposition_site_begin', site, desc(begin_date)), 
    )
    
    def __json__(self, request):
        return{
            'lat':self.lat,
            'lon':self.lon,
            'begin':self.begin_date,
            'end':self.end_date
        }