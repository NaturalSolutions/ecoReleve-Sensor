from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

### Create a database session : one for the whole application
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
_Base = declarative_base()
dbConfig = {
    'data_schema': 'ecoReleve_Data.dbo',
    'dialect': 'mssql',
    'sensor_schema': 'ecoReleve_Sensor.dbo'
}

from .rfid import Rfid