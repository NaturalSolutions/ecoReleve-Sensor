from pyramid.view import view_config
from sqlalchemy import select, distinct, join, text,Table, and_, bindparam, update, alias, cast, Time, String, Integer
from ecorelevesensor.models import *
import numpy as np
import sys, datetime, transaction
from sqlalchemy.sql import func
import json, os
from collections import OrderedDict

prefix = 'station'
dict_proto={
	'Biometry': TProtocolBirdBiometry,
	'Building and Activities':TProtocolBuildingAndActivity,
	'Capture Individual': TProtocolCaptureIndividual,
	'Chiro capture':TProtocolChiropteraCapture,
	'Chiro detection':TProtocolChiropteraDetection,
	'Clutch Description': TProtocolClutchDescription,
	# 'Entomo Pop Census': TSubProtocolEntomoPopCensus,
	'Entomo population': TProtocolEntomoPopulation,
	'Habitat description':TProtocolPhytosociologyHabitat,
	'Nest and clutch description': TProtocolNestDescription,
	'Phytosociology habitat': TProtocolPhytosociologyHabitat,
	'Phytosociology releve': TProtocolPhytosociologyReleve,
	'Plant inventory': TProtocolPhytosociologyReleve,
	'Vertebrate Release': TProtocolReleaseGroup,
	'Release Individual': TProtocolReleaseIndividual,
	'Simplified habitat':TProtocolSimplifiedHabitat,
	'Sighting conditions': TProtocolSightingCondition,
	'Simplified Habitat': TProtocolSimplifiedHabitat,
	'Station description':TProtocolStationDescription,
	'Station equipment': TProtocolStationEquipment,
	# 'SubProtocol Transect': TSubProtocolTransect,
	'Tracks and Clues': TProtocolTrackClue,
	'Transects': TProtocolTransect,
	'Vertebrate Aerian Individuals' : TProtocolVertebrateIndividual,
	'Vertebrate Capture': TProtocolCaptureGroup,
	'Vertebrate group': TProtocolVertebrateGroup,
	'Vertebrate Individual Death':TProtocolVertebrateIndividualDeath,
	'Vertebrate individual': TProtocolVertebrateIndividual
	}

def getWorkerID(workerList) :
	users_ID_query = select([User.id], User.fullname.in_((workerList)))
	users_ID = DBSession.execute(users_ID_query).fetchall()
	users_ID=[row[0] for row in users_ID]
	if len(users_ID) <3 :
		users_ID.extend([None,None])
	return users_ID

@view_config(route_name=prefix+'/protocol/data', renderer='json', request_method='PUT')
def insert_protocol (request):

	data=dict(request.params)
	proto_name = request.matchdict['name']
	# insert new row in the protocol
	new_proto=dict_proto[proto_name]()
	new_proto.InitFromFields(data)
	DBSession.add(new_proto)
	DBSession.flush()
	id_proto= new_proto.PK
	return id_proto

@view_config(route_name=prefix+'/protocol/data', renderer='json', request_method='POST')
def update_protocol (request):

	data = request.json_body
	proto_name = request.matchdict['name']
	pk_data = int(request.matchdict['PK_data'])
	id_station = int(request.matchdict['id'])
	# insert new row in the protocol
	if int(pk_data) == 0 :
		new_proto=dict_proto[proto_name]()
		data['FK_TSta_ID'] = id_station
		new_proto.InitFromFields(data)
		DBSession.add(new_proto)
		DBSession.flush()
		id_proto= new_proto.PK
	else :
		up_proto=DBSession.query(dict_proto[proto_name]).get(pk_data)
		data['FK_TSta_ID'] = id_station
		up_proto.InitFromFields(data)
		id_proto=up_proto.PK
		transaction.commit()
	return id_proto

@view_config(route_name=prefix+'/protocol', renderer='json', request_method='GET')
def get_protocol_on_station (request):

	id_station = int(request.matchdict['id'])
	table=Base.metadata.tables['V_TThem_Proto']
	query = select([table.c['proto_name'], table.c['proto_id'],table.c['proto_relation']]
		).where(table.c['proto_active'] == 1)
	proto_list = DBSession.execute(query.distinct()).fetchall()
	proto_on_sta = {}

	for name, Id, relation in proto_list :

		Tproto = Base.metadata.tables['TProtocol_'+relation]
		query_proto = select([Tproto.c['PK']]).where(Tproto.c['FK_TSta_ID']==id_station)
		PK_data = [row[0] for row in DBSession.execute(query_proto).fetchall()]

		if len(PK_data) > 0 : 	
			proto_on_sta[name] = {'id': Id, 'PK_data': PK_data }

	if proto_on_sta != {} :
		station = DBSession.query(Station).get(id_station)
		query = query.where(table.c['theme_name'] == station.fieldActivityName)
		proto_list = DBSession.execute(query.distinct()).fetchall()

		for name, Id, relation in proto_list : 
			if name not in proto_on_sta : 
				proto_on_sta[name] = {'id' : Id, 'PK_data': [0] }
		data=proto_on_sta
	else :

		station = DBSession.query(Station).get(id_station)
		query = query.where(table.c['theme_name'] == station.fieldActivityName)
		proto_list = DBSession.execute(query.distinct()).fetchall()

		for name, Id, relation in proto_list : 
			proto_on_sta[name] = {'id' : Id, 'PK_data': [0] }

	return proto_on_sta
		
@view_config(route_name=prefix+'/protocol/data', renderer='json', request_method='GET')
def get_data_on_protocol (request):
	
	id_station = int(request.matchdict['id'])
	proto_name = request.matchdict['name']
	pk_data = int(request.matchdict['PK_data'])
	table=Base.metadata.tables['TProtocole']

	proto_relation = DBSession.execute(select([table.c['Relation']]
			).where(table.c['Caption'] == proto_name)).fetchone()
	transaction.commit()

	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	with open(path+'/models/protocols/'+str(proto_relation[0]).lower()+'.json', 'r') as json_data:
		model_proto = json.load(json_data)

	if  pk_data != 0 :
		Tproto = dict_proto[proto_name]
		Tproto = Base.metadata.tables['TProtocol_'+str(proto_relation[0])]
		query_cols = []
		hour_cols =[]

		for col in Tproto.c : 
			if ('time' in col.name.lower() and 'DATETIME' in str(col.type).upper()
				) or ('hour' in col.name.lower() and 'DATETIME' in str(col.type).upper()) :
				hour_cols.append(col.name)
				query_cols.append(cast(Tproto.c[col.name],Time).label(col.name))
			elif str(col.type) == 'BIT':
				query_cols.append(cast(Tproto.c[col.name],Integer).label(col.name))
			else :	
				query_cols.append(Tproto.c[col.name])

		query = select(query_cols).where(Tproto.c['PK'] == pk_data)
		data = DBSession.execute(query).fetchall()
		datas = {}
		for row in data : 
			row = OrderedDict(row)
			if 'time' or 'hour' in [x.lower() for x in hour_cols] :
				for time_field in hour_cols :
					if row[time_field] != None :
						row[time_field] = row[time_field].strftime('%H:%M')
			datas.update(row)
		model_proto['data']= datas
	return model_proto

@view_config(route_name='protocols/list', renderer='json', request_method='GET')
def list_protocol (request):

	table=Base.metadata.tables['V_TThem_Proto']
	query = select([table.c['proto_name'], table.c['proto_id']]).where(table.c['proto_active'] == 1)
	data = DBSession.execute(query.distinct()).fetchall()
	return [OrderedDict(row) for row in data]
