"""
Created on Mon Aug 18 11:19:51 2014

@author: Natural Solutions (Thomas)
"""

from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings
from ecorelevesensor.models import Base, DBSession, dbConfig

import sys

if __name__ == '__main__':
    """Create all tables in the database."""
    settings = get_appsettings(sys.argv[1])
    dbConfig['data_schema'] = settings['data_schema']
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    from ecorelevesensor.models.data import *
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)