"""
Created on Thu Aug 28 16:53:04 2014

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

class ProtocolRfid(Base):
    __tablename__ = 'T_ProtocolRfid'
    pk_id = Column('PK_id', Integer, Sequence('seq_protocolrfid_pk_id'),
                   primary_key=True)
    fk_ant = Column('FK_ant', Integer)
    fk_ind = Column('Fk_ind', Integer)
    chip_code = Column(String(10), nullable=False)
    date = Column('date_', DateTime, nullable=False)
    lat = Column(Numeric(9,5))
    lon = Column(Numeric(9,5))
    area = Column(String)
    creation_date = Column(DateTime, server_default=func.now())
    creator = Column(Integer)
    if dialect.startswith('mssql'):
        __table_args__ = (
            Index(
                'idx_Tprotocolrfid_fkind_with_date_lat_lon',
                fk_ind,
                mssql_include=[date, lat, lon]
            ),
            UniqueConstraint(fk_ant, chip_code, date),
            {'schema': schema}
        )
    else:
        __table_args__ = (
            Index(
                'idx_Tprotocolrfid_fkind',
                fk_ind
            ),
            UniqueConstraint(fk_ant, chip_code, date),
            {'schema': schema}
        )
            