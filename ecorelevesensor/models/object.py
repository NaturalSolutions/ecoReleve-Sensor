"""
Created on Fri Aug 29 16:06:47 2014

@author: Natural Solutions (Thomas)
"""

from sqlalchemy import (
    Column,
    DateTime,
    func,
    Index,
    Integer,
    Numeric,
    Sequence,
    String,
    UniqueConstraint
)

from ecorelevesensor.models import Base, dbConfig

schema = dbConfig['data_schema']
dialect = dbConfig['dialect']

class Object(Base):
    __tablename__ = 'T_Object'
    pk_id = Column('PK_id', Integer, Sequence('seq_object_pk_id'),
                   primary_key=True)
    type_ = Column(String(16), nullable=False)
    constructor = Column(String(32))
    creation_date = Column(DateTime, server_default=func.now(), nullable=False)
    creator = Column(Integer, nullable=False)
    __table_args__ = (
            Index('idx_Tobject_type', type_),
            {'schema': schema}
    )
    __mapper_args__ = {
        'polymorphic_on':type_,
        'polymorphic_identity':'object'
    }
    
class Object_Rfid(Object):
    __mapper_args__ = {
        'polymorphic_identity':'rfid'
    }

class Object_Argos(Object):
    __mapper_args__ = {
        'polymorphic_identity':'argos'
    }
    
class Object_Gsm(Object):
    __mapper_args__ = {
        'polymorphic_identity':'gsm'
    }