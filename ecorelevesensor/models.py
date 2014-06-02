from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    String
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

class Individuals(Base):
   __tablename__ = 'TViewIndividual'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo'}
   id = Column('Individual_Obj_PK', Integer, primary_key = True)
   ptt = Column('id19@TCarac_PTT', Integer)
   sex = Column('id30@TCaracThes_Sex_Precision', String)
   age = Column('id2@Thes_Age_Precision', String)
   origin = Column('id33@Thes_Origin_Precision', String)
   specie = Column('id34@TCaracThes_Species_Precision', String)
   status = Column('id59@TCaracThes_Individual_Status', String)

class Sat_Trx(Base):
   __tablename__ = 'TViewTrx_Sat'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo'}
   id = Column('Trx_Sat_Obj_PK', Integer, primary_key = True)
   ptt = Column('id19@TCarac_PTT', Integer)
   manufacturer = Column('id42@TCaracThes_Company_Precision', String)
   model = Column('id41@TCaracThes_Model_Precision', String)

class Station(Base):
   __tablename__ = 'TStations'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo'}
   id = Column('TSta_PK_ID', Integer, primary_key = True)
   date = Column('DATE', DateTime)