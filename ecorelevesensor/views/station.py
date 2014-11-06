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
	DBSession)
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
	date=data.get('Date_')
	print (date)
	check_duplicate_station = select([func.count(Station.id)]).where(and_(Station.date == bindparam('date'),
		Station.lat == bindparam('lat'),Station.lon == bindparam('lon')))

	if DBSession.execute(check_duplicate_station, {'date':date, 'lat':data['LAT'], 'lon':data['LON']}).scalar() == 0:
		lastId=DBSession.query(func.max(Station.id)).one()
		lastId=lastId[0]+1
		print ('_____________________')
		print(lastId)
		# date=datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S ')
		station=Station(name=data['Name'],lat=data['LAT'], lon= data['LON'], date=date, fieldActivityName = data['FieldActivity_Name'],
			creator=request.authenticated_userid, updateRegion=0)

		DBSession.add(station)
		DBSession.flush()
		lastId=station.id
		print ('_____________________')
		print(lastId)
		return lastId
	else :
		return None

@view_config(route_name=prefix+'/checkStation', renderer='json', request_method='GET')
def check_newStation (request):
	print ('_____________________')

	data=request.params
	date=data.get('Date_')
	check_duplicate_station = select([func.count(Station.id)]).where(and_(Station.date == bindparam('date'),
		Station.lat == bindparam('lat'),Station.lon == bindparam('lon')))

	if DBSession.execute(check_duplicate_station, {'date':date, 'lat':data['LAT'], 'lon':data['LON']}).scalar() == 0:
		insertNewStation(request)
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
	print (data.get('protocolName'))

	new_proto=dict_proto[protocol]()
	setattr(new_proto,'FK_TSta_ID',data.get('TSta_PK_ID'))
	print(new_proto)
	field=json.loads(data.get('protocolForm'))
	new_proto.InitFromFields(field)

	# print (data.get('protocolName'))
	# print (field.items())
	print(new_proto)
	DBSession.add(new_proto)
	# print(Station.__mapper__)
	

	# proto_Name='TProtocol_'+data['protocolName'].replace(' ','_')
	# proto_field=json.loads(data.get('protocolForm'))
	# table=Base.metadata.tables[proto_Name]
	# print(table.c)
