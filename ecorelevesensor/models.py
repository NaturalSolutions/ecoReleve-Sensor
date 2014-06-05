from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    Sequence,
    Text,
    String
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
   backref,
   relationship,
   scoped_session,
   sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension
import decimal

# Create a database session : one for the whole application
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
   __table_args__ = {'schema': 'ecoReleve_Data.dbo', 'implicit_returning': False}
   id = Column('TSta_PK_ID', Integer, Sequence('TStations_pk_id'), primary_key = True)
   date = Column('DATE', DateTime, nullable = False)
   name = Column('Name', String)
   fieldActivityId = Column('FieldActivity_ID', Integer)
   fieldActivityName = Column('FieldActivity_Name', String)
   lat = Column('lat', Numeric(9,5), nullable = False)
   lon = Column('lon', Numeric(9,5), nullable = False)
   ele = Column('ele', Integer)
   precision = Column('Precision', Integer)
   creator = Column('Creator', Integer)
   creationDate = Column('Creation_date', DateTime)
   protocol_argos = relationship('ProtocolArgos', uselist=False, backref='Station')
   #protocol_gps = relationship('ProtocolGps', uselist=False, backref='station')

class ProtocolArgos(Base):
   __tablename__ = 'TProtocol_ArgosDataArgos'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo', 'implicit_returning': False}
   id = Column('PK', Integer, Sequence('TProtocol_ArgosDataArgos_pk_id'), primary_key = True)
   station_id = Column('FK_TSta_ID', Integer, ForeignKey(Station.id))
   ind_id = Column('FK_TInd_ID', Integer, nullable = False)
   lc = Column('TADA_LC', String(1))
   iq = Column('TADA_IQ', Integer)
   nbMsg = Column('TADA_NbMsg', Integer)
   nbMsg120 = Column('TADA_NbMsg>-120Db', Integer)
   bestLvl = Column('TADA_BestLevel', Integer)
   passDuration = Column('TADA_PassDuration', Integer)
   nopc = Column('TADA_NOPC', Integer)
   frequency = Column('TADA_Frequency', Numeric(10,1))
   comment = Column('TADA_Comments', String(250))

class ProtocolGps(Base):
   __tablename__ = 'TProtocol_ArgosDataGps'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo'}
   id = Column('PK', Integer, Sequence('TProtocol_ArgosDataGps_pk_id'), primary_key = True)
   station_id = Column('FK_TSta_ID', Integer, ForeignKey(Station.id))
   ind_id = Column('FK_TInd_ID', Integer, nullable = False)
   course = Column('TADG_Course', Integer)
   speed = Column('TADG_Speed', Integer)
   comment = Column('TADG_Comments', String(250))