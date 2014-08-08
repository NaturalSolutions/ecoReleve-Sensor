from sqlalchemy import Column, Integer, Table, Sequence, String
from ecorelevesensor.models import Base

# Specific SQL Server 
spatial_table = Table('spatial_temp', Base.metadata,
   Column('id', Integer, Sequence('spatial_temp_pk_id'), primary_key = True),
   Column('geo', String)
)