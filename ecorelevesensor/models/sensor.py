from sqlalchemy import (
   Boolean,
   Column,
   DateTime,
   Float,
   Index,
   Integer,
   Numeric,
   Sequence,
   String
 )

from ecorelevesensor.models import Base, dbConfig

sensor_schema = dbConfig['sensor_schema']
db_url = dbConfig['url']

class Argos(Base):
    __tablename__ = 'Targos'
    pk = Column('PK_id', Integer, Sequence('Targos_pk_id'), primary_key=True)
    ptt = Column('FK_ptt', Integer, nullable=False)
    date = Column('date', DateTime, nullable=False)
    lat = Column('lat', Numeric(9, 5), nullable=False)
    lon = Column('lon', Numeric(9, 5), nullable=False)
    ele = Column('ele', Integer)
    lc = Column('lc', String(1))
    iq = Column('iq', Integer)
    nbMsg = Column('nbMsg', Integer)
    nbMsg120 = Column('nbMsg>-120dB', Integer)
    bestLvl = Column('bestLevel', Integer)
    passDuration = Column('passDuration', Integer)
    nopc = Column('nopc', Integer)
    frequency = Column('freq', Float)
    checked = Column('checked', Boolean, nullable=False, default=False)
    imported = Column('imported', Boolean, nullable=False, default=False)
    if db_url.startswith('mssql'):
        __table_args__ = (
            Index(
                'idx_Targos_checked_with_pk_ptt_date',
                checked, 
                ptt,
                mssql_include=[pk, date]
            ),
            {'schema': sensor_schema}
        )
    else:
        __table_args__ = (
            Index('idx_Targos_checked_ptt', checked, ptt),
            {'schema': sensor_schema}
        )
       

class Gps(Base):
    __tablename__ = 'Tgps'
    pk = Column('PK_id', Integer, primary_key=True)
    ptt = Column('FK_ptt', Integer, nullable = False)
    date = Column('date', DateTime, nullable = False)
    lat = Column('lat', Numeric(9, 5), nullable = False)
    lon = Column('lon', Numeric(9, 5), nullable = False)
    ele = Column('ele', Integer)
    speed = Column('speed', Integer)
    course = Column('course', Integer)
    checked = Column('checked', Boolean, nullable = False, default = False)
    imported = Column('imported', Boolean, nullable = False, default = False)
    if db_url.startswith('mssql'):
        __table_args__ = (
            Index(
                'idx_Tgps_checked_with_pk_ptt_date',
                checked, 
                ptt,
                mssql_include=[pk, date]
            ),
            {'schema': sensor_schema}
        )
    else:
        __table_args__ = (
            Index('idx_Tgps_checked_ptt', checked, ptt),
            {'schema': sensor_schema}
        )

class Rfid(Base):
   __tablename__ = 'Trfid'
   __table_args__ = {'schema': 'ecoReleve_Sensor.dbo'}
   id = Column('PK_id', Integer, Sequence('Trfid_pk_id'), primary_key=True)
   code = Column('code', String, nullable=False)
   date = Column('date', DateTime, nullable=False)