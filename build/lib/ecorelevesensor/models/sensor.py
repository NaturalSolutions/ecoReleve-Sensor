from sqlalchemy import (
   Boolean,
   Column,
   DateTime,
   Float,
   Integer,
   Numeric,
   Sequence,
   String
 )

from sqlalchemy.orm import relationship
from ecorelevesensor.models import Base

class Argos(Base):
   __tablename__ = 'Targos'
   __table_args__ = {'schema': 'ecoReleve_Sensor.dbo'}
   id = Column('PK_id', Integer, primary_key=True)
   ptt = Column('FK_ptt', Integer, nullable = False)
   date = Column('date', DateTime, nullable = False)
   lat = Column('lat', Numeric(9, 5), nullable = False)
   lon = Column('lon', Numeric(9, 5), nullable = False)
   ele = Column('ele', Integer)
   lc = Column('lc', String(1))
   iq = Column('iq', Integer)
   nbMsg = Column('nbMsg', Integer)
   nbMsg120 = Column('nbMsg>-120dB', Integer)
   bestLvl = Column('bestLevel', Integer)
   passDuration = Column('passDuration', Integer)
   nopc = Column('nopc', Integer)
   frequency = Column('freq', Float)
   checked = Column('checked', Boolean, nullable = False, default = False)
   imported = Column('imported', Boolean, nullable = False, default = False)

class Gps(Base):
   __tablename__ = 'Tgps'
   __table_args__ = {'schema': 'ecoReleve_Sensor.dbo'}
   id = Column('PK_id', Integer, primary_key=True)
   ptt = Column('FK_ptt', Integer, nullable = False)
   date = Column('date', DateTime, nullable = False)
   lat = Column('lat', Numeric(9, 5), nullable = False)
   lon = Column('lon', Numeric(9, 5), nullable = False)
   ele = Column('ele', Integer)
   speed = Column('speed', Integer)
   course = Column('course', Integer)
   checked = Column('checked', Boolean, nullable = False, default = False)
   imported = Column('imported', Boolean, nullable = False, default = False)

class Rfid(Base):
   __tablename__ = 'Trfid'
   __table_args__ = {'schema': 'ecoReleve_Sensor.dbo'}
   id = Column('PK_id', Integer, Sequence('Trfid_pk_id'), primary_key=True)
   code = Column('code', String, nullable=False)
   date = Column('date', DateTime, nullable=False)