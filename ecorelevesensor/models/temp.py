from sqlalchemy import Column, Integer, Table
from ecorelevesensor.models import Base
from geoalchemy2 import Geometry

# Specific SQL Server 
spatial_table = Table('spatial_temp', Base.metadata,
   Column('id', Integer, primary_key = True),
   Column('geo', Geometry())
)