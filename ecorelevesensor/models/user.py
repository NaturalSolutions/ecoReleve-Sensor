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

db_dialect = dbConfig['dialect']

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
    if db_dialect =='mssql':
        __table_args__ = (
            Index('idx_Tuser_lastname_firstname', lastname, firstname, mssql_include=[id]),
            {'schema':dbConfig['data_schema']}
        )
    else:
        __table_args__ = (
            Index('idx_Tuser_lastname_firstname', lastname, firstname),
            {'schema':dbConfig['data_schema']}
        )

    @hybrid_property
    def fullname(self):
        """ Return the fullname of a user.
        """
        return self.lastname + ' ' + self.firstname
    
    def check_password(self, given_pwd):
        """Check the password of a user.
        
        Parameters
        ----------
        given_pwd : string
            The password to check, assumed to be an SHA1 hash of the real one.
            
        Returns
        -------
        boolean
            Either the password matches or not
        """
        return self.password == given_pwd.lower()
