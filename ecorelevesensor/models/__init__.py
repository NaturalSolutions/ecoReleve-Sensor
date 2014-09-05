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

from .animal import Animal
from .animal_location import AnimalLocation
from .monitored_site import MonitoredSite
from .monitored_site_position import MonitoredSitePosition
from .object import ObjectRfid
#from .station import Station
from .data_rfid import DataRfid
from .monitored_site_equipment import MonitoredSiteEquipment
from .user import User