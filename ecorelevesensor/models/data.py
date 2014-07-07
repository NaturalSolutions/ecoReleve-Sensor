from sqlalchemy import (
   Boolean,
   Column,
   DateTime,
   Float,
   ForeignKey,
   Integer,
   Numeric,
   Sequence,
   String,
   Table
 )

from sqlalchemy.orm import relationship
from ecorelevesensor.models import Base, dbConfig

data_schema = dbConfig['data_schema']

class Station(Base):
   __tablename__ = 'TStations'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo', 'implicit_returning': False}
   id = Column('TSta_PK_ID', Integer, Sequence('TStations_pk_id'), primary_key = True)
   date = Column('DATE', DateTime, nullable = False)
   name = Column('Name', String)
   area = Column('Area', String)
   fieldActivityId = Column('FieldActivity_ID', Integer)
   fieldActivityName = Column('FieldActivity_Name', String)
   lat = Column('lat', Numeric(9,5), nullable = False)
   lon = Column('lon', Numeric(9,5), nullable = False)
   ele = Column('ele', Integer)
   precision = Column('Precision', Integer)
   creator = Column('Creator', Integer)
   creationDate = Column('Creation_date', DateTime)
   protocol_argos = relationship('ProtocolArgos', uselist=False, backref='Station')
   protocol_gps = relationship('ProtocolGps', uselist=False, backref='Station')

class ProtocolIndividualEquipment(Base):
   __tablename__ =  'TProtocol_Individual_Equipment'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo', 'implicit_returning': False}
   id = Column('PK_ID', Integer, Sequence('TProtocol_Individual_Equipment_pk_id'), primary_key = True)
   sat_id = Column('FK_SAT_ID', Integer)
   ind_id = Column('FK_IND_ID', Integer)
   begin_date = Column(DateTime)
   end_date = Column(DateTime)

class SatTrx(Base):
   __tablename__ = 'TViewTrx_Sat'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo'}
   id = Column('Trx_Sat_Obj_PK', Integer, primary_key = True)
   ptt = Column('id19@TCarac_PTT', Integer)
   manufacturer = Column('id42@TCaracThes_Company_Precision', String)
   model = Column('id41@TCaracThes_Model_Precision', String)

class Individuals(Base):
   __tablename__ = 'TViewIndividual'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo'}
   id = Column('Individual_Obj_PK', Integer, primary_key = True)
   ptt = Column('id19@TCarac_PTT', Integer)
   age = Column('id2@Thes_Age_Precision', String)
   sex = Column('id30@TCaracThes_Sex_Precision', String)
   release_ring_code = Column('id9@TCarac_Release_Ring_Code', String)
   origin = Column('id33@Thes_Origin_Precision', String)
   specie = Column('id34@TCaracThes_Species_Precision', String)
   status = Column('id59@TCaracThes_Individual_Status', String)
   monitoring_status = Column('id60@TCaracThes_Monitoring_Status_Precision', String)
   survey_type = Column('id61@TCaracThes_Survey_type_Precision', String)

class ProtocolGps(Base):
   __tablename__ = 'TProtocol_ArgosDataGps'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo', 'implicit_returning': False}
   id = Column('PK', Integer, Sequence('TProtocol_ArgosDataGps_pk_id'), primary_key = True)
   station_id = Column('FK_TSta_ID', Integer, ForeignKey(Station.id))
   ind_id = Column('FK_TInd_ID', Integer, nullable = False)
   course = Column('TADG_Course', Integer)
   speed = Column('TADG_Speed', Integer)
   comment = Column('TADG_Comments', String(250))

class ProtocolArgos(Base):
   __tablename__ = 'TProtocol_ArgosDataArgos'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo', 'implicit_returning': False}
   id = Column('PK', Integer, Sequence('TProtocol_ArgosDataArgos_pk_id'), primary_key = True)
   station_id = Column('FK_TSta_ID', Integer, ForeignKey(Station.id))
   ind_id = Column('FK_TInd_ID', Integer, nullable = False)
   lc = Column('TADA_LC', String(1))
   iq = Column('TADA_IQ', Integer)
   nbMsg = Column('TADA_NbMsg', Integer)
   nbMsg120 = Column('TADA_NbMsg>-120Db', Integer)
   bestLvl = Column('TADA_BestLevel', Integer)
   passDuration = Column('TADA_PassDuration', Integer)
   nopc = Column('TADA_NOPC', Integer)
   frequency = Column('TADA_Frequency', Numeric(10,1))
   comment = Column('TADA_Comments', String(250))

class ProtocolReleaseIndividual(Base):
   __tablename__ = 'TProtocol_Release_Individual'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo', 'implicit_returning': False}
   id = Column('PK', Integer, Sequence('TProtocol_Release_Individual_pk_id'), primary_key = True)
   station_id = Column('FK_TSta_ID', Integer, ForeignKey(Station.id), nullable = False)
   ind_id = Column('FK_TInd_ID', Integer, ForeignKey(Individuals.id), nullable = False)

class ProtocolCaptureIndividual(Base):
   __tablename__ = 'TProtocol_Capture_Individual'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo', 'implicit_returning': False}
   id = Column('PK', Integer, Sequence('TProtocol_Capture_Individual_pk_id'), primary_key = True)
   station_id = Column('FK_TSta_ID', Integer, ForeignKey(Station.id), nullable = False)
   ind_id = Column('FK_TInd_ID', Integer, ForeignKey(Individuals.id), nullable = False)

##### Views #####
V_AllIndivs_Released_YearArea = Table('V_Qry_AllIndivs_Released_YearArea', Base.metadata,
                                      Column('FK_TInd_ID', ForeignKey(Individuals.id)),
                                      schema=data_schema, autoload=True)

V_Search_Indiv = Table('V_Search_Indiv', Base.metadata,
                       Column('id', Integer, primary_key = True),
                       Column('ptt', Integer),
                       Column('releaseYear', Integer),
                       Column('captureYear', Integer),
                       schema=data_schema, autoload=True)

TViewStations = Table('TViewStations', Base.metadata,
                      Column('FK_IND_ID', Integer),
                      Column('lat', Numeric),
                      Column('lon', Numeric),
                      Column('date', DateTime),
                      schema=data_schema)

class ViewRfid(Base):
   __tablename__ = 'TViewRFID'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo'}
   id = Column('RFID_Obj_pk', Integer, primary_key = True)
   serial_number = Column('id65@TCarac_rfid_Serial_number',Integer)
   model = Column('id41@TCaracThes_Model',Integer)
   model_precision = Column('id41@TCaracThes_Model_Precision',String(50))
   company = Column('id42@TCaracThes_Company',Integer)
   company_precision = Column('id42@TCaracThes_Company_Precision',String(50))
   comment = Column('id37@Comments',String)
   protocolStationEquipment_rfid = relationship('ProtocolStationEquipment', uselist=False, backref='ViewRfid.id')

class MonitoredStation(Base):
   __tablename__ = 'TMonitoredStations'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo'}
   id = Column('TGeo_pk_id', Integer, primary_key = True)
   name = Column('Name', String(50))
   creation_date = Column('Creation_date',DateTime)
   creator = Column('Creator',Integer)
   active = Column('Active', Integer)
   id_type = Column('id_Type', Integer)
   name_type = Column('name_Type',String(50))
   protocolStationEquipment_geo = relationship('ProtocolStationEquipment', uselist=False, backref='MonitoredStation.id')

class ProtocolStationEquipment(Base):
   __tablename__ = 'TProtocol_Station_equipment_new'
   __table_args__ = {'schema': 'ecoReleve_Data.dbo', 'implicit_returning': False}
   id = Column('PK_id',Integer, Sequence('TProtocol_Station_equipment_new_pk_id'), primary_key = True)
   fk_rfid = Column(Integer, ForeignKey(ViewRfid.id))
   fk_geo = Column(Integer, ForeignKey(MonitoredStation.id))
   begin_date = Column('beginDATE', DateTime, nullable = False)
   end_date = Column('endDATE', DateTime, nullable = True)