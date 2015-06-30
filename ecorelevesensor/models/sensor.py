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
dialect = dbConfig['dialect']

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
    if dialect.startswith('mssql'):
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
    checked = Column('checked', Boolean, nullable=False, default=False)
    imported = Column('imported', Boolean, nullable=False, default=False)
    if dialect.startswith('mssql'):
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
        
class ArgosGps(Base):
    __tablename__ = 'T_argosgps'
    pk_id = Column('PK_id', Integer, primary_key=True)
    ptt = Column('FK_ptt', Integer, nullable = False)
    type_ = Column('type',String(3), nullable = False)
    date = Column('date', DateTime, nullable = False)
    lat = Column(Numeric(9, 5), nullable = False)
    lon = Column(Numeric(9, 5), nullable = False)
    ele = Column(Integer)
    speed = Column(Integer)
    course = Column(Integer)
    lc = Column('lc', String(1))
    iq = Column('iq', Integer)
    nbMsg = Column(Integer)
    nbMsg120 = Column(Integer)
    bestLvl = Column('bestLevel', Integer)
    passDuration = Column(Integer)
    nopc = Column('nopc', Integer)
    frequency = Column('freq', Float)
    checked = Column('checked', Boolean, nullable=False, default=False)
    imported = Column('imported', Boolean, nullable=False, default=False)
    if dialect.startswith('mssql'):
        __table_args__ = (
            Index(
                'idx_Targosgps_checked_with_pk_ptt_date',
                checked, 
                ptt,
                mssql_include=[pk_id, date]
            ),
            {'schema': sensor_schema}
        )
    else:
        __table_args__ = (
            Index('idx_Targosgps_checked_ptt', checked, ptt),
            {'schema': sensor_schema}
        )
        
class Gsm(Base):
    __tablename__ = 'Tgsm'
    pk_id = Column('PK_id', Integer, primary_key=True)
    fk_ptt = Column('FK_ptt', Integer, nullable = False)
    date = Column('date_', DateTime, nullable = False)
    lat = Column(Numeric(9, 5), nullable = False)
    lon = Column(Numeric(9, 5), nullable = False)
    ele = Column(Integer)
    speed = Column(Integer)
    course = Column(Integer)
    checked = Column(Boolean, nullable=False, default=False)
    imported = Column(Boolean, nullable=False, default=False)
    if dialect.startswith('mssql'):
        __table_args__ = (
            Index('idx_Tgsm_checked_with_pk_ptt_date', checked, fk_ptt,
                mssql_include=[pk_id, date]
            ),
            {'schema': sensor_schema}
        )
    else:
        __table_args__ = (
            Index('idx_Tgsm_checked_ptt', checked, fk_ptt),
            {'schema': sensor_schema}
        )


class ArgosEngineering(Base):
    __tablename__ = 'Tgps_engineering'
    pk_id = Column('PK_id', Integer, primary_key=True)
    fk_ptt = Column('FK_ptt', Integer, nullable = False)
    pttDate = Column('pttDate', DateTime, nullable = False)
    txDate = Column('txDate', DateTime, nullable = False)
    satId = Column(String)
    txCount = Column(Integer)
    temp = Column(Float)
    batt = Column(Float)
    fixTime = Column(Integer)
    satCount = Column(Integer)
    resetHours = Column(Integer)
    fixDays = Column(Integer)
    season = Column(Integer)
    shunt = Column(Boolean)
    mortalityGT = Column(Boolean)
    seasonalGT = Column(Boolean)
    latestLat = Column(Float)
    latestLon = Column(Float)

    __table_args__ = (
        Index('idx_Tgps_engineering_pttDate_ptt', pttDate, fk_ptt),
        {'schema': sensor_schema}
    )
