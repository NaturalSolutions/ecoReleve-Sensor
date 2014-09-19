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
    String,
    Table,
    func
)
from sqlalchemy.orm import relationship

from ecorelevesensor.models import Base

class Station(Base):
    __tablename__ = 'TStations'
    id = Column('TSta_PK_ID', Integer, Sequence('TStations_pk_id'), primary_key = True)
    date = Column('DATE', DateTime, nullable = False)
    name = Column('Name', String)
    area = Column('Region', String)
    fieldActivityId = Column('FieldActivity_ID', Integer)
    fieldActivityName = Column('FieldActivity_Name', String)
    lat = Column(Numeric(9,5), nullable = False)
    lon = Column(Numeric(9,5), nullable = False)
    ele = Column(Integer)
    precision = Column('Precision', Integer)
    creator = Column('Creator', Integer)
    creationDate = Column('Creation_date', DateTime, server_default=func.now())
    protocol_argos = relationship('ProtocolArgos', uselist=False, backref='Station')
    protocol_gps = relationship('ProtocolGps', uselist=False, backref='Station')
    
    def __json__(self, request):
        return {
            'id': self.id,
            'date': str(self.date),
            'lat': float(self.lat),
            'lon': float(self.lon)
        }