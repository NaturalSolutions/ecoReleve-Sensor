"""
Created on Fri Sep 19 17:24:09 2014
@author: Natural Solutions (Thomas)
"""

from pyramid.view import view_config
from sqlalchemy import select, distinct, join, text,Table, and_, bindparam
from ecorelevesensor.models import (TProtocolBirdBiometry,
	TProtocolChiropteraCapture,TProtocolSimplifiedHabitat,
	TProtocolChiropteraDetection,TProtocolBuildingAndActivity,
	TProtocolVertebrateIndividualDeath, TProtocolStationDescription,
	Station, Individual,
	Base,
	DBSession,
	User)
import numpy as np
import datetime
from sqlalchemy.sql import func
import json
prefix = 'station'

@view_config(route_name=prefix, renderer='json', request_method='GET')
def monitoredSites(request):
   
	data = DBSession.query(Station).all()
	return data

@view_config(route_name=prefix+'/id', renderer='json', request_method='GET')
def monitoredSite(request):
   
	id_ = request.matchdict['id']
	print(id_)
	print(Station)
	data = DBSession.query(Station).filter(Station.id == id_).one()
	return data

	
@view_config(route_name=prefix+'/area', renderer='json', request_method='GET')
def monitoredSitesArea(request):	

	proto_view_Name=request.matchdict['name_vue']
	proto_view_Table=Base.metadata.tables[proto_view_Name]
	join_table=proto_view_Table.join(Station, proto_view_Table.c['TSta_PK_ID'] == Station.id )
	
	slct=select([Station.area]).distinct().select_from(join_table)
	data = DBSession.execute(slct).fetchall()

	return [row['Region' or 'Area'] for row in data]


@view_config(route_name=prefix+'/locality', renderer='json', request_method='GET')
def monitoredSitesLocality(request):
	
	proto_view_Name=request.matchdict['name_vue']
	proto_view_Table=Base.metadata.tables[proto_view_Name]
	join_table=proto_view_Table.join(Station, proto_view_Table.c['TSta_PK_ID'] == Station.id )
	
	slct=select([Station.locality]).distinct().select_from(join_table)
	data = DBSession.execute(slct).fetchall()

	return [row['Place' or 'Locality'] for row in data]

@view_config(route_name=prefix+'/addStation', renderer='json', request_method='POST')
def insertNewStation(request):

	data=request.params
	check_duplicate_station = select([func.count(Station.id)]).where(and_(Station.date == bindparam('date'),
		Station.lat == bindparam('lat'),Station.lon == bindparam('lon')))

	if DBSession.execute(check_duplicate_station, {'date':data['Date_'], 'lat':data['LAT'], 'lon':data['LON']}).scalar() == 0:

		# get userID with fieldWorker_Name
		users_ID_query = select([User.id], User.fullname.in_((data['FieldWorker1'],data['FieldWorker2'],data['FieldWorker3'])))
		users_ID = DBSession.execute(users_ID_query).fetchall()
		users_ID=[row[0] for row in users_ID]
		if len(users_ID) <3 :
			users_ID.extend([None,None])

		station=Station(name=data['Name'],lat=data['LAT'], lon= data['LON'], 
			date=data['Date_'], fieldActivityName = data['FieldActivity_Name'],
			creator=request.authenticated_userid, updateRegion=0,
			fieldWorker1=users_ID[0],fieldWorker2=users_ID[1],fieldWorker3=users_ID[2])

		DBSession.add(station)
		DBSession.flush()
		id_sta=station.id
	
		print(id_sta)
		return id_sta
	else :
		return None

@view_config(route_name=prefix+'/searchStation', renderer='json', request_method='GET')
def check_newStation (request):
	print ('_____________________')

	data=request.params
	check_duplicate_station = select([func.count(Station.id)]).where(and_(Station.date == bindparam('date'),
		Station.lat == bindparam('lat'),Station.lon == bindparam('lon')))

	if DBSession.execute(check_duplicate_station, {'date':data['Date_'], 'lat':data['LAT'], 'lon':data['LON']}).scalar() == 0:
		return 0
	else :

		return 1


@view_config(route_name=prefix+'/addProtocol', renderer='json', request_method='POST')
def insert_protocol (request):
	print('----_____----')

	dict_proto={
	'Bird Biometry': TProtocolBirdBiometry,
	'Chiroptera capture':TProtocolChiropteraCapture,
	'Simplified Habitat':TProtocolSimplifiedHabitat,
	'Chiroptera detection':TProtocolChiropteraDetection,
	'Building and Activities':TProtocolBuildingAndActivity,
	'station description':TProtocolStationDescription,
	'Vertebrate individual death':TProtocolVertebrateIndividualDeath
	}
	data=request.params
	protocol=data.get('protocolName')

	# insert new row in the protocol
	try :
		new_proto=dict_proto[protocol]()
		setattr(new_proto,'FK_TSta_ID',data.get('TSta_PK_ID'))
		field=json.loads(data.get('protocolForm'))
		new_proto.InitFromFields(field)
		DBSession.add(new_proto)
	except :
		raise

@view_config(route_name=prefix+'/updateProtocol', renderer='json', request_method='POST')
def uptdate_protocol (request):

	date=request.params
	up_proto=dict_proto[data.get('protocolName')]

@view_config(route_name=prefix+'/updateProtocol', renderer='json', request_method='GET')
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


@view_config(route_name=prefix+'/station_byDate', renderer='json', request_method='GET')
def station_byDate (request) :

	data=reques.params

	query= select(Station).filter(Station.date>=data.get('begin_date')).filter(Station.date<=data.get('end_date'))
	result= DBSession.execute(query).fetchall()
    
	return result