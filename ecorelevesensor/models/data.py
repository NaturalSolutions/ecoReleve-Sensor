from sqlalchemy import (
	Boolean,
	Column,
	DateTime,
	ForeignKey,
	Integer,
	Numeric,
	Sequence,
	String,
	Table,
	distinct,
	select
 )

from ecorelevesensor.models import Base
from .individual import Individual
from .station import Station

class ProtocolIndividualEquipment(Base):
	__tablename__ =  'TProtocol_Individual_Equipment'
	id = Column('PK_ID', Integer, Sequence('TProtocol_Individual_Equipment_pk_id'), primary_key = True)
	sat_id = Column('FK_SAT_ID', Integer)
	ind_id = Column('FK_IND_ID', Integer)
	begin_date = Column(DateTime)
	end_date = Column(DateTime)

class SatTrx(Base):
	__tablename__ = 'TViewTrx_Sat'
	id = Column('Trx_Sat_Obj_PK', Integer, primary_key = True)
	ptt = Column('id19@TCarac_PTT', Integer)
	manufacturer = Column('id42@TCaracThes_Company_Precision', String)
	model = Column('id41@TCaracThes_Model_Precision', String)

class CaracTypes(Base):
	__tablename__ = 'TObj_Carac_type'
	id = Column('Carac_type_Pk', Integer, Sequence('TObj_Carac_type_pk_id'), primary_key=True)
	label = Column('label', String)

class ObjectsCaracValues(Base):
	__tablename__ = 'TObj_Carac_value'
	id = Column('Carac_value_Pk', Integer, Sequence('TObj_Carac_value_pk_id'), primary_key=True)
	object = Column('fk_object', Integer)
	carac_type = Column('Fk_carac', Integer, ForeignKey(CaracTypes.id))
	object_type = Column('object_type', String)
	value = Column('value', String)
	value_precision = Column('value_precision', String)
	begin_date = Column(DateTime)
	end_date = Column(DateTime)

class ProtocolGps(Base):
	__tablename__ = 'TProtocol_ArgosDataGps'
	id = Column('PK', Integer, Sequence('TProtocol_ArgosDataGps_pk_id'), primary_key=True)
	station_id = Column('FK_TSta_ID', Integer, ForeignKey(Station.id))
	ind_id = Column('FK_TInd_ID', Integer, nullable=False)
	course = Column('TADG_Course', Integer)
	speed = Column('TADG_Speed', Integer)
	comment = Column('TADG_Comments', String(250))

class ProtocolArgos(Base):
	__tablename__ = 'TProtocol_ArgosDataArgos'
	id = Column('PK', Integer, Sequence('TProtocol_ArgosDataArgos_pk_id'), primary_key=True)
	station_id = Column('FK_TSta_ID', Integer, ForeignKey(Station.id))
	ind_id = Column('FK_TInd_ID', Integer, nullable=False)
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
	id = Column('PK', Integer, Sequence('TProtocol_Release_Individual_pk_id'), primary_key = True)
	station_id = Column('FK_TSta_ID', Integer, ForeignKey(Station.id), nullable = False)
	ind_id = Column('FK_TInd_ID', Integer, ForeignKey(Individual.id), nullable = False)

class ProtocolCaptureIndividual(Base):
	__tablename__ = 'TProtocol_Capture_Individual'
	id = Column('PK', Integer, Sequence('TProtocol_Capture_Individual_pk_id'), primary_key = True)
	station_id = Column('FK_TSta_ID', Integer, ForeignKey(Station.id), nullable = False)
	ind_id = Column('FK_TInd_ID', Integer, ForeignKey(Individual.id), nullable = False)

##### Views #####
"""
V_AllIndivs_Released_YearArea = Table('V_Qry_AllIndivs_Released_YearArea', Base.metadata,
												  Column('FK_TInd_ID', ForeignKey(Individual.id)),
												  schema=data_schema, autoload=True)
"""

V_Individuals_LatLonDate = Table('V_Individuals_LatLonDate', Base.metadata,
							 Column('ind_id', Integer),
							 Column('lat', Numeric),
							 Column('lon', Numeric),
							 Column('date', DateTime))

V_Individuals_History = Table('V_Individuals_History', Base.metadata,
										Column('ind_id', Integer, key='id'),
										Column('Fk_carac', Integer, key='carac'),
										Column('value', String),
										Column('begin_date', DateTime),
										Column('end_date', DateTime),
										Column('label', String))

V_Individuals_Stations = Table('V_Individuals_Stations', Base.metadata,
										 Column('ind_id', Integer),
										 Column('sta_id', Integer),
										 Column('fk_sta_type', Integer))

class ViewRfid(Base):
	__tablename__ = 'TViewRFID'
	id = Column('RFID_Obj_pk', Integer, primary_key = True)
	serial_number = Column('id65@TCarac_rfid_Serial_number',Integer)
	model = Column('id41@TCaracThes_Model',Integer)
	model_precision = Column('id41@TCaracThes_Model_Precision',String(50))
	company = Column('id42@TCaracThes_Company',Integer)
	company_precision = Column('id42@TCaracThes_Company_Precision',String(50))
	comment = Column('id37@Comments',String)

class ThemeEtude(Base):
	__tablename__ = 'TThemeEtude'
	id = Column('TProt_PK_ID', Integer, primary_key = True)
	Caption = Column('Caption', String)
	Definition_fr = Column('Definition_fr', String)
	Bibliography = Column('Bibliography', String)
	Creation_date = Column('Creation_date', DateTime)
	Creator = Column('Creator', String)
	Actif = Column('Actif', Boolean)
	NeedGeom = Column('NeedGeom', Boolean)
	Definition_en = Column('Definition_en', String)

class MapSelectionManager(Base):
	__tablename__ = 'TMapSelectionManager'
	id = Column('TSMan_ID', Integer, primary_key = True)
	TSMan_sp_name = Column('TSMan_sp_name', String)
	TSMan_Layer_Name = Column('TSMan_Layer_Name', String)
	TSMan_Description = Column('TSMan_Description', String)
	TSMan_FK_Theme = Column(Integer, ForeignKey(ThemeEtude.id))
	TSMan_AdminQry = Column('TSMan_AdminQry', Boolean)

class Protocole(Base):
	__tablename__ = 'TProtocole'
	id = Column('TTheEt_PK_ID', Integer, primary_key = True)
	Relation = Column('Relation', String)
	Caption = Column('Caption', String)
	Description = Column('Description', String)
	Active = Column(Boolean)
	Creation_date = Column('Creation_date', DateTime)
	Creator = Column('Creator', String)
	Support = Column('Support', String)


