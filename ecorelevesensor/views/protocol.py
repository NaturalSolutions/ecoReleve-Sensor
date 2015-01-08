from pyramid.view import view_config
from sqlalchemy import select, distinct, join, text,Table, and_, bindparam, update, alias
from ecorelevesensor.models import *
import numpy as np
import sys, datetime, transaction
from sqlalchemy.sql import func
import json, os
from collections import OrderedDict

prefix = 'station'
dict_proto={
	'Bird Biometry': TProtocolBirdBiometry,
	'Chiroptera capture':TProtocolChiropteraCapture,
	'Simplified Habitat':TProtocolSimplifiedHabitat,
	'Chiroptera detection':TProtocolChiropteraDetection,
	'Building and Activities':TProtocolBuildingAndActivity,
	'station description':TProtocolStationDescription,
	'Vertebrate individual death':TProtocolVertebrateIndividualDeath,
	'Phytosociology habitat': TProtocolPhytosociologyHabitat,
	'Phytosociology releve': TProtocolPhytosociologyReleve,
	'Sighting conditions': TProtocolSightingCondition,
	'Simplified Habitat': TProtocolSimplifiedHabitat,
	'Station equipment': TProtocolStationEquipment,
	'Track clue': TProtocolTrackClue,
	'Capture Group': TProtocolCaptureGroup,
	'Capture Individual': TProtocolCaptureIndividual,
	'Nest Description': TProtocolNestDescription,
	'Clutch Description': TProtocolClutchDescription,
	'Entomo population': TProtocolEntomoPopulation,
	# 'Entomo Pop Census': TSubProtocolEntomoPopCensus,
	'Release Group': TProtocolReleaseGroup,
	'Release Individual': TProtocolReleaseIndividual,
	'Transects': TProtocolTransect,
	# 'SubProtocol Transect': TSubProtocolTransect,
	'Vertebrate group': TProtocolVertebrateGroup,
	'Vertebrate individual': TProtocolVertebrateIndividual
	}

def getWorkerID(workerList) :
	users_ID_query = select([User.id], User.fullname.in_((workerList)))
	users_ID = DBSession.execute(users_ID_query).fetchall()
	users_ID=[row[0] for row in users_ID]
	if len(users_ID) <3 :
		users_ID.extend([None,None])
	return users_ID

@view_config(route_name=prefix+'/addProtocol', renderer='json', request_method='POST')
def insert_protocol (request):
	data=dict(request.params)
	protocolName=data['name']
	# insert new row in the protocol
	if request.params.has_key('PK')!=True :
		
		new_proto=dict_proto[protocolName]()
		new_proto.InitFromFields(data)
		DBSession.add(new_proto)
		DBSession.flush()
		id_proto= new_proto.PK
		print(id_proto)
		return id_proto

	else :

		up_proto=DBSession.query(dict_proto[protocolName]).get(data['PK'])
		del data['name'],data['PK'],data['FK_TSta_ID']
		print(up_proto)
		up_proto.InitFromFields(data)
		id_proto=up_proto.PK
		transaction.commit()

		return id_proto

@view_config(route_name=prefix+'/protocol', renderer='json', request_method='GET')
def get_protocol_on_station (request):

	id_station = request.matchdict['id']
	table=Base.metadata.tables['V_TThem_Proto']
	print(id_station)

	query = select([table.c['proto_name'], table.c['proto_id'],table.c['proto_relation']]
		).where(table.c['proto_active'] == 1)
	proto_list = DBSession.execute(query.distinct()).fetchall()
	proto_on_sta = {}

	for name, Id, relation in proto_list :

		Tproto = Base.metadata.tables['TProtocol_'+relation]
		query_proto = select([Tproto.c['PK']]).where(Tproto.c['FK_TSta_ID']==id_station)
		PK_data = [row[0] for row in DBSession.execute(query_proto).fetchall()]
		
		print(len(PK_data))

		if len(PK_data) > 0 : 	
			proto_on_sta[name] = {'id': Id, 'PK_data': PK_data }

	if proto_on_sta != {} :
		print('\n\n____________protocol exists for station _____________\n\n')
		data=proto_on_sta

	else :

		station = DBSession.query(Station).get(id_station)
		print('\n\n____________NO NO NO protocol exists for station _____________\n\n')
		print (station.fieldActivityName)

		query = query.where(table.c['theme_name'] == station.fieldActivityName)
		proto_list = DBSession.execute(query.distinct()).fetchall()

		for name, Id, relation in proto_list : 
			proto_on_sta[name] = {'id' : Id, 'PK_data': [0] }

	return proto_on_sta
		

@view_config(route_name=prefix+'/protocol/data', renderer='json', request_method='GET')
def get_data_on_protocol (request):
	

	id_station = request.matchdict['id']
	proto_name = request.matchdict['name']
	pk_data = request.matchdict['PK_data']

	print ('\n\n________protocol/DATA____________\n')
	print(id_station)
	print(proto_name)
	print(pk_data)

	table=Base.metadata.tables['V_TThem_Proto']

	proto_relation = DBSession.execute(select([table.c['proto_relation']]
			).where(table.c['proto_name'] == proto_name)).fetchone()
	print (proto_relation)
	transaction.commit()

	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	with open(path+'/models/protocols/'+str(proto_relation[0]).lower()+'.json', 'r') as json_data:
		model_proto = json.load(json_data)

	if  pk_data != 0 :
	
		Tproto = Base.metadata.tables['TProtocol_'+str(proto_relation[0])]
		query = select([Tproto]).where(Tproto.c['PK'] == pk_data)
		data = DBSession.execute(query).fetchall()
		print (data)
		model_proto['data']=[OrderedDict(row) for row in data]

	return model_proto


@view_config(route_name='protocols/list', renderer='json', request_method='GET')
def list_protocol (request):

	table=Base.metadata.tables['V_TThem_Proto']

	query = select([table.c['proto_name'], table.c['proto_id']]).where(table.c['proto_active'] == 1)
	data = DBSession.execute(query.distinct()).fetchall()

	return [OrderedDict(row) for row in data]
