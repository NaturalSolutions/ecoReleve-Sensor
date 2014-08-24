from sqlalchemy import (
   Column,
   DateTime,
   Index,
   Integer,
   Sequence,
   String,
   Table,
   func
 )

from sqlalchemy.ext.hybrid import hybrid_property
from ecorelevesensor.models import Base, dbConfig

class User(Base):
    __tablename__ = 'T_User'
    id = Column('PK_id', Integer, Sequence('seq_user_pk_id'), primary_key=True)
    lastname = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    creation_date = Column(DateTime, nullable=False,
                           server_default=func.now())
    login = Column('login_', String, nullable=False)
    password = Column('password_', String, nullable=False)
    language = Column('language_', String(2))
    __table_args__ = (
        Index('idx_TUser_lastname_firstname', lastname, firstname),
        {'schema':dbConfig['data_schema']}
    )

    @hybrid_property
    def fullname(self):
        return self.lastname + ' ' + self.firstname

    #TUse_Departement = Column('TUse_Departement', String)
    #TUse_Fonction = Column('TUse_Fonction', String)
    #TUse_Actif = Column('TUse_Actif')
