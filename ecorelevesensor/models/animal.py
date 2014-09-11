from sqlalchemy import (
   Column,
   Index,
   Integer,
   Sequence,
   String,
 )

from ecorelevesensor.models import Base

class Animal(Base):
    #TODO: Ajouter un autoincrément à la fin d'eRelevé
    __tablename__ = 'T_Animal'
    id = Column('PK_id', Integer, primary_key=True)
    chip_code = Column(String(10))
    __table_args__ = (
        Index('idx_Tanimal_chipcode_pk', chip_code, id),
    )