from sqlalchemy import (
   Boolean,
   Column,
   DateTime,
   Float,
   ForeignKey,
   Index,
   Integer,
   Numeric,
   Sequence,
   String,
   Table,
   func
 )

from sqlalchemy.orm import relationship
from ecorelevesensor.models import Base, dbConfig

schema = dbConfig['data_schema']

