from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension
import decimal

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Argos(Base):
	__tablename__ = 'Targos'
	__table_args__ = {'schema': 'ecoReleve_Sensor.dbo'}
	id = Column('PK_id', Integer, primary_key=True)
	ptt = Column('FK_ptt', Integer, nullable = False)
	date = Column('date', DateTime, nullable = False)
	lat = Column('lat', Numeric(9, 5), nullable = False)
	lon = Column('lon', Numeric(9, 5), nullable = False)
	ele = Column('ele', Integer)
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

class Bird(Base):
   __tablename__ = 'TViewIndividual'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo'}
   id = Column('Individual_Obj_PK', Integer, primary_key = True)
   ptt = Column('id19@TCarac_PTT', Integer)