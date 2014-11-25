"""
Created on Fri Sep 19 17:24:09 2014
@author: Natural Solutions (Thomas)
"""

from pyramid.view import view_config
from sqlalchemy import select, distinct, join, text,Table, and_, bindparam, update, func
from ecorelevesensor.models import * 
import sys, datetime, transaction
from sqlalchemy.sql import func
import json,datetime
prefix = 'station'

def getFieldActitityID (data) :

	id_field_query=select([ThemeEtude.id], ThemeEtude.Caption == data['FieldActivity_Name'])
	id_field=DBSession.execute(id_field_query).scalar()
	return id_field

def getRegion(lat,lon) :
	stmt_Region = text("""
		DECLARE @geoPlace varchar(255);
		EXEC dbo.sp_GetRegionFromLatLon :lat, :lon, @geoPlace OUTPUT;
		SELECT @geoPlace;"""
	).bindparams(bindparam('lat', value=lat , type_=Numeric(9,5)),bindparam('lon', value=lon , type_=Numeric(9,5)))
	geoRegion=DBSession.execute(stmt_Region).scalar()
	print (geoRegion)
	return geoRegion

def getUTM(lat,long) :
	stmt_UTM=text("""
		DECLARE @geoPlace varchar(255);
		EXEC dbo.sp_GetUTMCodeFromLatLon   :lat, :lon, @geoPlace OUTPUT;
		SELECT @geoPlace;"""
	).bindparams(bindparam('lat', value=lat, type_=Numeric(9,5)),bindparam('lon', value=lon , type_=Numeric(9,5)))
	geoUTM=DBSession.execute(stmt_UTM).scalar()
	print (geoUTM)
	return geoUTM

def getWorkerID(workerList) :
	users_ID_query = select([User.id], User.fullname.in_((workerList)))
	users_ID = DBSession.execute(users_ID_query).fetchall()
	users_ID=[row[0] for row in users_ID]
	if len(users_ID) <3 :
		users_ID.extend([None,None])
	return users_ID

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

	
@view_config(route_name=prefix+'/area', renderer='json', request_method='POST')
def monitoredSitesArea(request):

	req = request.POST

	if 'name_view' in req :
		print('name_view')
		try :
			proto_view_Table = Base.metadata.tables[proto_view_Name]
			join_table = join(proto_view_Table, Station, proto_view_Table.c['TSta_PK_ID'] == Station.id )
		except :
			proto_view_Table = dict_proto[proto_view_Name]()
			join_table = join(proto_view_Table, Station, proto_view_Table.FK_TSta_ID == Station.id )

		print (proto_view_Table)

	
		slct = select([Station.area]).distinct().select_from(join_table)
		data = DBSession.execute(slct).fetchall()
		return [row['Region' or 'Area'] for row in data]


	else :
		table = Base.metadata.tables['geo_CNTRIES_and_RENECO_MGMTAreas']
		slct = select([table.c['Country']]).distinct()
		data =  DBSession.execute(slct).fetchall()
		return [row[0] for row in data]



@view_config(route_name=prefix+'/locality', renderer='json', request_method='POST')
def monitoredSitesLocality(request):

	req = request.POST

	if 'name_view' in req :
		print('name_view')
		try :
			proto_view_Table=Base.metadata.tables[proto_view_Name]
			join_table=join(proto_view_Table, Station, proto_view_Table.c['TSta_PK_ID'] == Station.id )

		except :
			
			proto_view_Table=dict_proto[proto_view_Name]()
			join_table=join(proto_view_Table, Station, proto_view_Table.FK_TSta_ID == Station.id )

		slct=select([Station.locality]).distinct().select_from(join_table)
		data = DBSession.execute(slct).fetchall()
		return [row['Place' or 'Locality'] for row in data]
	else :
		table = Base.metadata.tables['geo_CNTRIES_and_RENECO_MGMTAreas']
		if 'Region' in req :
			query=select([table.c['Place']]).distinct().where(table.c['Country']==req.get('Region'))
		else :
			query=select([table.c['Place']]).distinct()
		data=DBSession.execute(query).fetchall()
		return [row[0] for row in data]



@view_config(route_name=prefix+'/addStation', renderer='json', request_method='POST')
def insertNewStation(request):

	data=dict(request.params)
	print(data)
	check_duplicate_station = select([func.count(Station.id)]).where(and_(Station.date == bindparam('date'),
		Station.lat == bindparam('lat'),Station.lon == bindparam('lon')))
	date=data.get('Date_')
	print (data)
	print(date)
	if 'PK' not in data :

		if (data['LON'],data['LAT'])!=('NULL','NULL') :

			if DBSession.execute(check_duplicate_station, {'date':date, 'lat':data['LAT'], 'lon':data['LON']}).scalar() == 0 :

				# get REGION and UTM by stored procedure
				print ('_______Region___________')
				stmt_Region = text("""
					DECLARE @geoPlace varchar(255);
					EXEC dbo.sp_GetRegionFromLatLon :lat, :lon, @geoPlace OUTPUT;
					SELECT @geoPlace;"""
				).bindparams(bindparam('lat', value=data['LAT'] , type_=Numeric(9,5)),bindparam('lon', value=data['LON'] , type_=Numeric(9,5)))
				geoRegion=DBSession.execute(stmt_Region).scalar()
				print (geoRegion)

				print ('_______UTM___________')
				stmt_UTM=text("""
					DECLARE @geoPlace varchar(255);
					EXEC dbo.sp_GetUTMCodeFromLatLon   :lat, :lon, @geoPlace OUTPUT;
					SELECT @geoPlace;"""
				).bindparams(bindparam('lat', value=data['LAT'] , type_=Numeric(9,5)),bindparam('lon', value=data['LON'] , type_=Numeric(9,5)))
				geoUTM=DBSession.execute(stmt_UTM).scalar()
				locality=None
				print (geoUTM)

			else :
				return 'a station exists at same date and coordinates'

		else :
			geoUTM=None
			geoRegion=data['Region']
			data['LAT'] = None
			data['LON'] = None

		#get userID with fieldWorker_Name
		users_ID_query = select([User.id], User.fullname.in_((data['FieldWorker1'],data['FieldWorker2'],data['FieldWorker3'])))
		users_ID = DBSession.execute(users_ID_query).fetchall()
		users_ID=[row[0] for row in users_ID]
		if len(users_ID) <3 :
			users_ID.extend([None,None])

		#get ID fieldActivity
		id_field_query=select([ThemeEtude.id], ThemeEtude.Caption == data['FieldActivity_Name'])
		id_field=DBSession.execute(id_field_query).scalar()

		# set station and insert it
		station=Station(name=data['Name'],lat=data['LAT'], lon= data['LON'], 
			date=data['Date_'], fieldActivityName = data['FieldActivity_Name'],
			creator=request.authenticated_userid, area=geoRegion, utm=geoUTM, fieldActivityId=id_field,
			fieldWorker1=users_ID[0],fieldWorker2=users_ID[1],fieldWorker3=users_ID[2])

		DBSession.add(station)
		DBSession.flush()
		id_sta=station.id
	
		print(id_sta)
		# return id_sta
		return {'PK':id_sta,'Region':geoRegion,'utm':geoUTM}
			
	elif 'PK' in data :
		
		print('_______________________')
		print(type(data['PK']))
		up_station=DBSession.query(Station).get(data['PK'])
		
		data['date']=data['Date_']
		del data['Date_'],data['PK'],data['FieldWorker4'],data['FieldWorker5'],data['FieldWorkersNumber']
		if data['LAT']=='NULL':
			data['LAT']=None
			data['LON']=None

		colToAttr=dict({v.name:k for k,v in up_station.__mapper__.c.items()})

		for k, v in data.items() :
			if 'FieldWorker' in k :
				v=getWorkerID([v])[0]
			setattr(up_station,colToAttr[k],v)
			print(k+' : ')
		up_station.fieldActivityId=getFieldActitityID(data)

		print (up_station.fieldActivityName)
		transaction.commit()
		return 'station updated with success'

	


@view_config(route_name=prefix+'/addMultStation', renderer='json', request_method='POST')
def insertMultStation(request):

	data=list(request.params)
	print (type(data))
	data=json.loads(data[0])
	print(data[0])
	check_duplicate_station = select([func.count(Station.id)]).where(and_(Station.date == bindparam('date'),
		Station.lat == bindparam('lat'),Station.lon == bindparam('lon')))

	creation_date=datetime.datetime.now()
	userID=getWorkerID([data[0]['fieldWorker1'],data[0]['fieldWorker2'],data[0]['fieldWorker3']])
	col=tuple(['Name','date','LAT','LON','Creation_date','FieldWorker1','FieldWorker2','FieldWorker3','Creator', 'Region'])
	print (creation_date)
	final=[dict(zip(col,[
		row['name']
		,datetime.datetime.strptime(row['waypointTime'].replace('-','/'),'%Y/%m/%d %H:%M:%S')
		,row['latitude']
		,row['longitude']
		,creation_date
		,userID[0]
		,userID[1]
		,userID[2]
		,request.authenticated_userid
		,getRegion(row['latitude'],row['longitude'])])) for row in data 
	if DBSession.execute(check_duplicate_station, {'date':datetime.datetime.strptime(row['waypointTime'],'%Y-%m-%d %H:%M:%S'), 'lat':row['latitude'], 'lon':row['longitude']}).scalar() == 0 ]

	query_insert=Station.__table__.insert()
	pkList=query_insert.execute(final)

	query=select([Station.id,Station.name,Station.date, Station.lat,Station.lon, Station.fieldWorker1,Station.fieldWorker2,Station.fieldWorker3,Station.fieldActivityName,Station.area,Station.utm]
		).where(and_(Station.creationDate==creation_date, Station.creator==request.authenticated_userid))
	pkIDs=DBSession.execute(query).fetchall()
	result=[{'PK':pk, 'Name':name, 'Date_': d.strftime('%d/%m/%Y %H:%M:%S'),'LAT':lat, 'LON':lon,'FieldWorker1':data[0]['fieldWorker1'],'FieldWorker2':data[0]['fieldWorker2'],'FieldWorker3':data[0]['fieldWorker3'],'FieldActivity_Name':fname, 'Region':area, 'UTM':utm} for pk,name,d,lat,lon,f1,f2,f3,fname,area,utm in pkIDs]
	return {
	'response':str(len(final))+' stations was added with succes, '+str(len(data)-len(final))+' are already existing',
	'data': result }


@view_config(route_name=prefix+'/searchStation', renderer='json', request_method='GET')
def check_newStation (request):
	print ('_________Search Station____________')

	data=request.params
	check_duplicate_station = select([func.count(Station.id)]).where(and_(Station.date == bindparam('date'),
		Station.lat == bindparam('lat'),Station.lon == bindparam('lon')))

	if DBSession.execute(check_duplicate_station, {'date':data['Date_'], 'lat':data['LAT'], 'lon':data['LON']}).scalar() == 0:
		return 0
	else :

		return 1


@view_config(route_name=prefix+'/station_byDate', renderer='json', request_method='GET')
def station_byDate (request) :

	data=reques.params

	query= select(Station).filter(Station.date>=data.get('begin_date')).filter(Station.date<=data.get('end_date'))
	result= DBSession.execute(query).fetchall()
    
	return result