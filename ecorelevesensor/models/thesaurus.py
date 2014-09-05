"""
Created on Mon Sep  1 14:53:26 2014

@author: Natural Solutions (Thomas)
"""

from sqlalchemy import (
    Column,
    DateTime,
    func,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    Sequence,
    String,
    UniqueConstraint
)

from ..models import Base, dbConfig
from .user import User

schema = dbConfig['data_schema']
dialect = dbConfig['dialect']

class Thesaurus(Base):
    __tablename__ = 'T_Thesaurus'
    pk_id = Column('PK_id', Integer, Sequence('seq_thesaurus_pk_id'),
                   primary_key=True)
    creator = Column('FK_creator', Integer, ForeignKey(User.id))
    modifier = Column('FK_modifier', Integer, ForeignKey(User.id))
    type_ = Column(Integer, nullable=False)
    parent = Column(Integer, nullable=False)
    hierarchy = Column(String(64), nullable=False)
    topic_fr = Column(String(256), nullable=False)
    topic_en = Column(String(256), unique=True, nullable=False)
    definition_fr = Column(String)
    definition_en = Column(String)
    reference = Column(String)
    creation_date = Column(DateTime, server_default=func.now())
    modification_date = Column(DateTime)
    __table_args__ = {'schema':schema}