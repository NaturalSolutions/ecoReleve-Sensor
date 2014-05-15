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
    __table_args__ = {'schema': 'ECWP_eReleve_Sensor.dbo'}
    id = Column('PK_id', Integer, primary_key=True)
    ptt = Column('FK_ptt', Integer)
    date = Column('date', DateTime, nullable = False)
    lat = Column('lat1', Numeric(9, 5), nullable = False)
    lon = Column('lon1', Numeric(9, 5), nullable = False)
    checked = Column('checked', Boolean, nullable = False, default = False)
    imported = Column('imported', Boolean, nullable = False, default = False)