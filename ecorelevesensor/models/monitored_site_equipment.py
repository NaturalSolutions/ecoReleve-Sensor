from sqlalchemy import (
   Boolean,
   Column,
   CheckConstraint,
   DateTime,
   Float,
   ForeignKey,
   Index,
   Integer,
   Numeric,
   Sequence,
   String,
   Table,
   func
 )

from ..models import Base, dbConfig
from .object import Object
from .monitored_site import MonitoredSite
from .user import User

schema = dbConfig['data_schema']

class MonitoredSiteEquipment(Base):
    __tablename__ = 'T_MonitoredSiteEquipment'
    id = Column('PK_id',Integer, Sequence('seq_monitoredsiteequipment_pk_id'),
                primary_key=True)
    obj = Column('FK_obj', Integer, ForeignKey(Object.id), nullable=False)
    site = Column('FK_site', Integer, ForeignKey(MonitoredSite.id), nullable=False)
    creator = Column('FK_creator', Integer, ForeignKey(User.id), nullable=False)
    creation_date = Column('creation_date', DateTime, server_default=func.now())
    lat = Column(Numeric(9,5), nullable=False)
    lon = Column(Numeric(9,5), nullable=False)
    begin_date = Column('begin_date', DateTime, nullable=False)
    end_date = Column('end_date', DateTime)

    __table_args__ = (
        CheckConstraint('end_date >= begin_date', 'end_date >= begin_date'),
        {'schema': schema}
    )

    def __json__(self, request):
        return {
            'id':self.id,
            'obj':self.obj,
            'site':self.site,
            'begin_date':str(self.begin_date),
            'end_date': None if self.end_date is None else str(self.end_date),
            'creator':self.creator,
            'creation_date':str(self.creation_date)
        }