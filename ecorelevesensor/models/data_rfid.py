"""
Created on Thu Aug 28 16:53:04 2014

@author: Natural Solutions (Thomas)
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
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
from ecorelevesensor.models.object import ObjectRfid

dialect = dbConfig['dialect']

class DataRfid(Base):
    __tablename__ = 'T_DataRfid'
    id = Column('PK_id', Integer, Sequence('seq_datarfid_pk_id'),
                   primary_key=True)
    creator = Column('FK_creator', Integer)
    obj = Column('FK_obj', Integer, ForeignKey(ObjectRfid.id), nullable=False)
    chip_code = Column(String(10), nullable=False)
    date = Column('date_', DateTime, nullable=False)
    creation_date = Column(DateTime, server_default=func.now())
    validated = Column(Boolean, server_default='0')
    __table_args__ = (
        Index('idx_Tdatarfid_chipcode_date', chip_code, date),
        UniqueConstraint(obj, chip_code, date),
    )
            