"""
Created on Mon Sep  1 14:38:09 2014

@author: Natural Solutions (Thomas)
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
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
from .user import User
from .thesaurus import Thesaurus

schema = dbConfig['data_schema']
dialect = dbConfig['dialect']

# TODO: homog�n�iser les notations � la fin d'eRelev�
class MonitoredSitePosition(Base):
    __tablename__ = 'TMonitoredStations_Positions'
    id = Column('TGeoPos_PK_ID', Integer, Sequence('seq_monitoredsiteposition_pk_id'),
                primary_key=True)
    creator = Column('FK_creator', Integer, ForeignKey(User.id))
    site = Column('TGeoPos_FK_TGeo_ID', Integer, ForeignKey(MonitoredSite.id), nullable=False)
    lat = Column('TGeoPos_LAT', Numeric(9,5), nullable=False)
    lon = Column('TGeoPos_LON', Numeric(9,5), nullable=False)
    ele = Column('TGeoPos_ELE', Float)
    precision = Column('TGeoPos_Precision', Integer)
    date = Column('TGeoPos_Date', DateTime)
    begin_date = Column('TGeoPos_Begin_Date', DateTime)
    end_date = Column('TGeoPos_End_Date', DateTime)
    comments = Column('TGeoPos_Comments', String)