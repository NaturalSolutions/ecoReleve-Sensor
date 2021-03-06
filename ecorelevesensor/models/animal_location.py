"""
Created on Wed Sep  3 10:14:05 2014

@author: Natural Solutions (Thomas)
"""

from sqlalchemy import (
    Column,
    DateTime,
    desc,
    ForeignKey,
    func,
    Index,
    Integer,
    Numeric,
    Sequence,
    String,
    UniqueConstraint
)

from ecorelevesensor.models import Base, dbConfig
from ecorelevesensor.models.object import Object
from .individual import Individual

dialect = dbConfig['dialect']

class AnimalLocation(Base):
    __tablename__ = 'T_AnimalLocation'
    pk_id = Column('PK_id', Integer, Sequence('seq_animallocation_pk_id'),
                   primary_key=True)
    creator = Column('FK_creator', Integer, nullable=False)
    obj = Column('FK_obj', Integer, ForeignKey(Object.id), nullable=False)
    ind = Column('FK_ind', Integer, ForeignKey(Individual.id), nullable=False)
    type_ = Column(String(8))
    date = Column('date_', DateTime, nullable=False)
    lat = Column(Numeric(9,5), nullable=False)
    lon = Column(Numeric(9,5), nullable=False)
    creation_date = Column(DateTime, server_default=func.now())
    if dialect.startswith('mssql'):
        __table_args__ = (
            Index(
                'idx_Tanimallocation_ind_date_with_lat_lon',
                ind, desc(date),
                mssql_include=[lat, lon]
            ),
            UniqueConstraint(ind, obj, date),
        )
    else:
        __table_args__ = (
            Index(
                'idx_Tanimallocation_fkind',
                ind, desc(date)
            ),
            UniqueConstraint(ind, obj, date),
        )