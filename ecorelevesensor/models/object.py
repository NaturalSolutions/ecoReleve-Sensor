"""
Created on Fri Aug 29 16:06:47 2014

@author: Natural Solutions (Thomas)
"""

from sqlalchemy import (
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

dialect = dbConfig['dialect']

class Object(Base):
    __tablename__ = 'T_Object'
    id = Column('PK_id', Integer, Sequence('seq_object_pk_id'),
                   primary_key=True)
    creator = Column('FK_creator', Integer, nullable=False)
    creation_date = Column(DateTime, server_default=func.now(), nullable=False)
    identifier = Column(String(32), nullable=False)
    type_ = Column(String(16), nullable=False)
    manufacturer = Column(String(64))
    model = Column(String(64))
    __table_args__ = (
            Index('idx_Tobject_type_identifier', type_, identifier),
            UniqueConstraint('identifier'),
    )
    __mapper_args__ = {
        'polymorphic_on':type_,
        'polymorphic_identity':'object'
    }

    def __json__(self, request):
        return {
            'id':self.id,
            'manufacturer':self.manufacturer,
            'model':self.model,
            'creator':self.creator,
            'identifier':self.identifier,
            'type':self.type_,
            'creation_date':str(self.creation_date),
        }
    
class ObjectRfid(Object):
    __mapper_args__ = {
        'polymorphic_identity':'rfid'
    }
    
class Transmitter(Object):
    platform_id = Column(Integer)
    
    def __json__(self, request):
        obj = super().__json__(request)
        obj['platform_id'] = self.platform_id
        return obj
    
    __mapper_args__ = {
        'polymorphic_identity':'transmitter'
    }

class ObjectArgos(Transmitter):
    program_id = Column(Integer)
    __mapper_args__ = {
        'polymorphic_identity':'argos'
    }
    
class ObjectGsm(Transmitter):
    serial_number = Column(String(32))
    
    def __json__(self, request):
        obj = super().__json__(request)
        obj['serial_number'] = self.serial_number
        return obj
    
    __mapper_args__ = {
        'polymorphic_identity':'gsm'
    }