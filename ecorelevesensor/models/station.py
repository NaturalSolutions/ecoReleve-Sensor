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
    func,
    text
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql.base import BIT
from ..models import Base

class Station(Base):
    __tablename__ = 'TStations'
    id = Column('TSta_PK_ID', Integer, Sequence('TStations_pk_id'), primary_key=True)
    date = Column(DateTime, index=True, nullable=False)
    name = Column('Name', String)
    area = Column('Region', String)
    locality = Column('Place', String)
    utm=Column('UTM20',String)
    fieldActivityId = Column('FieldActivity_ID', Integer)
    fieldActivityName = Column('FieldActivity_Name', String)
    fieldWorker1= Column('FieldWorker1', Integer)
    fieldWorker2= Column('FieldWorker2', Integer)
    fieldWorker3= Column('FieldWorker3', Integer)
    lat = Column(Numeric(9,5), nullable=False)
    lon = Column(Numeric(9,5), nullable=False)
    ele = Column(Integer)
    precision = Column('Precision', Integer)
    creator = Column('Creator', Integer)
    updateRegion=Column('regionUpdate',BIT,server_default=text("((0))"))
    creationDate = Column('Creation_date', DateTime, server_default=func.now())
    protocol_argos = relationship('ProtocolArgos', uselist=False, backref='station')
    protocol_gps = relationship('ProtocolGps', uselist=False, backref='station')
    
    def __json__(self, request):
        return {
            'id': self.id,
            'date': str(self.date),
            'lat': float(self.lat),
            'lon': float(self.lon)
        }