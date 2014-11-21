from pyramid.view import view_config
from sqlalchemy import select, distinct, join, text,Table, and_, bindparam, update
from ecorelevesensor.models import *
import numpy as np
import sys, datetime, transaction
from sqlalchemy.sql import func
import json
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
		print('_______add proto_____')
		new_proto=dict_proto[protocolName]()
		new_proto.InitFromFields(data)
		DBSession.add(new_proto)
		DBSession.flush()
		id_proto= new_proto.PK
		print(id_proto)
		return id_proto
	else :
		print('_______update proto__________')
		up_proto=DBSession.query(dict_proto[protocolName]).get(data['PK'])
		del data['name'],data['PK'],data['FK_TSta_ID']
		print(up_proto)
		up_proto.InitFromFields(data)
		id_proto=up_proto.PK
		transaction.commit()

		return id_proto
@view_config(route_name=prefix+'/getProtocol', renderer='json', request_method='GET')
def get_protocol (request):

	data=request.params
	id_sta=data.get('id_sta')
	proto_onSta={}
	for protoName, Tproto in dict_proto :
		print(protoName+' : '+ Tproto)
		query=select(Tproto,Tproto.FK_TSta_ID==id_sta)
		res=DBSession.execute(query).scalar()
		print(res)
		if res!=None :
			proto_onSta[protoName]=res
	
	return proto_onSta