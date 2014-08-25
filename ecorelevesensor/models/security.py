from sqlalchemy import (
   Column,
   DateTime,
   Index,
   Integer,
   Sequence,
   String,
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
    role = Column('role_', String(16), nullable=False)
    __table_args__ = (
        Index('idx_Tuser_lastname_firstname', lastname, firstname),
        {'schema':dbConfig['data_schema']}
    )

    @hybrid_property
    def fullname(self):
        return self.lastname + ' ' + self.firstname
    
    def check_password(self, given_pwd):
        """Check the password of an user.
        
        Parameters
        ----------
        given_pwd : string
            The password to check, assumed to be an SHA1 hash of the real one.
            
        Returns
        -------
        boolean
            Either the password matches or not
        """
        return self.password == given_pwd
"""
class Role(Base):
    __tablename__ = 'T_Role'
    id = Column('PK_id', Integer, Sequence('seq_role_pk_id'), primary_key=True)
    name = Column(String(32), nullable=False)
    __table_args__ = {'schema':dbConfig['data_schema']}
"""    
    #TUse_Departement = Column('TUse_Departement', String)
    #TUse_Fonction = Column('TUse_Fonction', String)
    #TUse_Actif = Column('TUse_Actif')
