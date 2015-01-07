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

@view_config(route_name=prefix+'/getProtocol', renderer='json', request_method='GET')
def get_protocol (request):

	data=dict(request.GET)
	print(data)
	id_sta=data.get('id_sta', None)
	id_proto=data.get('id_proto',None)
	proto_name = data.get('proto_name',None)
	table=Base.metadata.tables['V_TThem_Proto']
	print(id_sta)
	print(id_proto)
	print(proto_name)
	

	# for protoName, Tproto in dict_proto.items() :
	# 		query=select([Tproto]).where(Tproto.FK_TSta_ID==id_sta)
	# 		protoOnSta.update({protoName: [dict(row) for row in DBSession.execute(query).fetchall()]})
	# print(protoOnSta)
	# return protoOnSta

	query = select([table.c['proto_name'], table.c['proto_id'],table.c['proto_relation']]
		).where(table.c['proto_active'] == 1)
	

	if proto_name == None :
		proto_list = DBSession.execute(query.distinct()).fetchall()
		protoOnSta={}
		for name, Id, relation in proto_list :
			Tproto = Base.metadata.tables['TProtocol_'+relation]
			query = select([Tproto.c['PK']]).where(Tproto.c['FK_TSta_ID']==id_sta)
			PK_data = [row[0] for row in DBSession.execute(query).fetchall()]
			if len(PK_data) > 0 : 
				protoOnSta[name] = {'id': Id, 'PK_data': PK_data }


	elif proto_name != None : 
		
		proto_relation = DBSession.execute(select([table.c['proto_relation']]
			).where(table.c['proto_name'] == proto_name)).fetchone()
		print (proto_relation)
		transaction.commit()

		path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		with open(path+'/models/protocols/'+str(proto_relation[0]).lower()+'.json') as json_data:
			
			model_proto = json.load(json_data)

		if  id_proto != '' :
			id_proto=int(id_proto)
			Tproto = Base.metadata.tables['TProtocol_'+str(proto_relation[0])]
			query = select([Tproto]).where(Tproto.c['PK'] == id_proto)
			data = DBSession.execute(query).fetchall()
			print (data)
			model_proto['data']=[OrderedDict(row) for row in data]

		return model_proto


@view_config(route_name='protocols/list', renderer='json', request_method='GET')
def list_protocol (request):

	data=dict(request.GET)
	fieldActivity=data.get('fieldActivity',None)
	id_sta=data.get('id_sta', None)
	table=Base.metadata.tables['V_TThem_Proto']

	if id_station == None and fieldActivity != None :
		query = select([table.c['proto_name'], table.c['proto_id']]).where(and_(table.c['proto_active'] == 1, table.c['theme_name'] == fieldActivity))
		data = DBSession.execute(query.distinct()).fetchall()

	elif id_sta != None :

		query = select([table.c['proto_name'], table.c['proto_id'],table.c['proto_relation']]
		).where(table.c['proto_active'] == 1)

		proto_list = DBSession.execute(query.distinct()).fetchall()
		protoOnSta={}
		for name, Id, relation in proto_list :
			Tproto = Base.metadata.tables['TProtocol_'+relation]
			query = select([Tproto.c['PK']]).where(Tproto.c['FK_TSta_ID']==id_sta)
			PK_data = [row[0] for row in DBSession.execute(query).fetchall()]
			if len(PK_data) > 0 : 
				protoOnSta[name] = {'id': Id, 'PK_data': PK_data }
		data = protoOnSta
	
	else :
		query = select([table.c['proto_name'], table.c['proto_id']]).where(table.c['proto_active'] == 1)
		data = DBSession.execute(query.distinct()).fetchall()

	return [OrderedDict(row) for row in data]
