"""
Created on Sat Sep  6 15:33:49 2014

@author: Natural Solutions (Thomas)
"""

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
   func
 )

from ecorelevesensor.models import Base, dbConfig

schema = dbConfig['data_schema']

class Individual(Base):
    __tablename__ = 'TViewIndividual'
    id = Column('Individual_Obj_PK', Integer, Sequence('seq_individual_pk_id'),
                primary_key=True)
    ptt = Column('id19@TCarac_PTT', Integer)
    age = Column('id2@Thes_Age_Precision', String)
    birth_date = Column('id35@Birth_date', DateTime)
    sex = Column('id30@TCaracThes_Sex_Precision', String)
    frequency = Column('id5@TCarac_Transmitter_Frequency', Integer)
    chip_code = Column('id13@TCarac_Chip_Code', String)
    breeding_ring = Column('id12@TCarac_Breeding_Ring_Code', String)
    release_ring = Column('id9@TCarac_Release_Ring_Code', String)
    origin = Column('id33@Thes_Origin_Precision', String)
    specie = Column('id34@TCaracThes_Species_Precision', String)
    status = Column('id59@TCaracThes_Individual_Status', String)
    survey_type = Column('id61@TCaracThes_Survey_type_Precision', String)
    monitoring_status = Column('id60@TCaracThes_Monitoring_Status_Precision',
                               String)
    survey_type = Column('id61@TCaracThes_Survey_type_Precision', String)
    history = []
    __table_args__ = ({'schema':schema})
    
    def __json__(self, request):
        return {
            'id':self.id,
            'ptt':self.ptt,
            'age':self.age,
            'birth_date': str(self.birth_date) if self.birth_date is not None else None,
            'history':self.history,
            'monitoring_status': self.monitoring_status,
            'origin':self.origin,
            'sex':self.sex,
            'specie':self.specie,
            'status':self.status,
            'survey_type':self.survey_type
        }