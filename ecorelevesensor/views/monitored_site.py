"""
Created on Mon Sep  1 17:28:02 2014

@author: Natural Solutions (Thomas)
"""
from ecorelevesensor.utils.generator import Generator
from pyramid.view import view_config
from sqlalchemy import select, distinct, join, and_, desc, func
from ecorelevesensor.models import DBSession, MonitoredSite, MonitoredSitePosition
import json
from ecorelevesensor.models import Base, DBSession

from collections import OrderedDict

prefix = 'monitoredSite'


gene= Generator('V_Qry_MonitoredSites_V2')

@view_config(route_name=prefix, renderer='json', request_method='GET')
def monitoredSites(request):
	data = DBSession.query(MonitoredSite).order_by(MonitoredSite.name).all()
	return data

@view_config(route_name=prefix+'/id', renderer='json', request_method='GET')
def monitoredSite(request):
	id_ = request.matchdict['id']
	data = DBSession.query(MonitoredSite).filter(MonitoredSite.id == id_).order_by(MonitoredSite.name).one()
	return data
	
@view_config(route_name=prefix+'/list', renderer='json', request_method='POST')
def monitoredSite_post(request):
	cols = request.json_body['cols']
	order = request.json_body['order']
	select_clause = []
	for col in cols:
		if col in MonitoredSite.__table__.c:
			select_clause.append(MonitoredSite.__table__.c[col])
	query = select(select_clause)
	for ord in order:
		if ord in MonitoredSite.__table__.c:
			query = query.order_by(MonitoredSite.__table__.c[ord])
	data = DBSession.execute(query).fetchall()
	return [dict(site) for site in data]
	
@view_config(route_name=prefix+'/list', renderer='json', request_method='GET')
def monitoredSite_list(request):
	query = select(MonitoredSite.__table__.c).order_by(MonitoredSite.name)
	data = DBSession.execute(query).fetchall()
	return [dict(site) for site in data]
	
@view_config(route_name=prefix+'/name', renderer='json')
def monitoredSite_name(request):

	typeSite=request.params.get('type')
	print(typeSite)
	query =select([MonitoredSite.name]
		).order_by(MonitoredSite.name)

	if typeSite!=None:
		query=query.where(MonitoredSite.type_==typeSite)
		data = DBSession.execute(query).fetchall()
		return [row['name'] for row in data]
	else :
		data = DBSession.execute(query).fetchall()
		return [site['name'] for site in data]


@view_config(route_name=prefix+'/type', renderer='json')
def monitored_site(request):
	data = DBSession.execute(select([distinct(MonitoredSite.type_
		).label('FK_type')]).order_by('FK_type')).fetchall()
	return [row[0] for row in data]

@view_config(route_name=prefix+'/info', renderer='json')
def monitoredSite_byName(request):

	nameSite=request.params.get('name')
	typeSite=request.params.get('type')
	query=select([MonitoredSitePosition.lat.label('lat'),MonitoredSitePosition.lon.label('lon')
		, MonitoredSite.id.label('id_site'),MonitoredSitePosition.ele.label('ele'),MonitoredSitePosition.precision.label('precision')]
		).select_from(join(MonitoredSitePosition, MonitoredSite , MonitoredSitePosition.site == MonitoredSite.id)
		).where(and_(MonitoredSite.name==nameSite, MonitoredSite.type_==typeSite)).order_by(desc(MonitoredSitePosition.begin_date))

	data = DBSession.execute(query).first()

	return dict([ (key,val) for key,val in data.items()])





@view_config(route_name=prefix+'/search', renderer='json')
def monitoredSite_search(request):

	print('________Search___________')


	try:
		criteria = json.loads(request.GET.get('criteria',{}))
	except:
		criteria={}
		
<<<<<<< HEAD
	for obj in criteria :
		if obj['Column'] == 'Status' :
			obj['Column'] = 'Active'
			if(obj['Value'] == 'Active'): obj['Value'] = True
			else: obj['Value'] = False
=======
	print(criteria)
>>>>>>> 84875a88f0acdd616a16ec2644ca62078208fc06


	if(request.GET.get('offset')):
		offset = json.loads(request.GET.get('offset',{}))
		perPage = json.loads(request.GET.get('per_page',{}))
		orderBy = json.loads(request.GET.get('order_by',{}))
		content = gene.get_search(criteria, offset=offset, per_page=perPage, order_by=orderBy)
	else :
		content = gene.get_search(criteria)
	

	return content

@view_config(route_name=prefix + '/getFilters', renderer='json', request_method='GET')
def monitoredSite_filters(request):
	print('____________FIELDS_________________')
	table=Base.metadata.tables['V_Qry_MonitoredSites_V2']
	
	columns=table.c
	
	final={}
	for col in columns :
		name=col.name
		Ctype=str(col.type)
		if 'VARCHAR' in Ctype:
			Ctype='String'
		final[name]=Ctype

	return final


@view_config(route_name=prefix + '/search_geoJSON', renderer='json', request_method='GET')
def monitoredSite_geoJSON(request):


	table=Base.metadata.tables['V_Qry_MonitoredSites_V2']


	print(request.GET)

	try:
		criteria = json.loads(request.GET.get('criteria',{}))
	except:
		criteria={}

	for obj in criteria :
		if obj['Column'] == 'Status' :
			obj['Column'] = 'Active'
			if(obj['Value'] == 'Active'): obj['Value'] = True
			else: obj['Value'] = False

	if(request.GET.get('offset')):
		offset = json.loads(request.GET.get('offset',{}))
		print('_________________')
		print(offset)
		perPage = json.loads(request.GET.get('per_page',{}))
		orderBy = json.loads(request.GET.get('order_by',{}))
		content = gene.get_geoJSON(criteria, offset=offset, per_page=perPage, order_by=orderBy)
	else :
		content = gene.get_geoJSON(criteria)

	return content

@view_config(route_name=prefix + '/detail', renderer='json', request_method='GET')
def monitoredSite_detail(request):	
	id_ = request.matchdict['id']
	table = Base.metadata.tables['V_fullMonitoredSites']
	print('____________________fds')
	print(table.c)



	data = DBSession.execute(select([table]).where(table.c['id']==id_)).fetchall()
	print(data)
	#print(data['end_date'])
	print(type(data))
	print(data)
	result= []
	result.append([OrderedDict(row) for row in data])
	print(result)
	#result['end_date'] = data['end_date'].strftime('%m/%d/%Y')
	#result['begin_date'] = data['begin_date'].strftime('%m/%d/%Y')

	return result

@view_config(route_name=prefix + '/detail_geoJSON', renderer='json', request_method='GET')
def monitoredSite_detailGeoJSON(request):	
	id_ = request.matchdict['id']
	table = Base.metadata.tables['V_fullMonitoredSites']
	print('____________________test')
	print(id_)
	data = DBSession.execute(select([table]).where(table.c['id']==id_)).fetchall()
	print (data)
	geoJson=[]
	for row in data:
            geoJson.append({'type':'Feature', 'properties':{'id':row['id'], 'end': row['end_date'], 'begin': row['begin_date']}, 'geometry':{'type':'Point', 'coordinates':[row['lon'],row['lat']]}})
	return geoJson


@view_config(route_name=prefix + '/newSite', renderer='json', request_method='POST')
def monitoredSite_newSite(request):

	print ('new Site')
	data = request.json_body
	location = data['location']
	print(location)

	type_id = DBSession.execute(select([distinct(MonitoredSite.id_type
		)]).where(MonitoredSite.type_ == data['type'])).scalar()

	new_site = MonitoredSite(creator = request.authenticated_userid, type_ = data['type'], id_type = type_id
		, name = data['name'], active = data['active'])

	DBSession.add(new_site)
	DBSession.flush()
	data['id'] = new_site.id
	if (location != None) :
		data['location']['site'] = new_site.id
		return monitoredSite_newLocation(data, new_site.id)
	else :
		return data

@view_config(route_name=prefix + '/newLocation', renderer='json', request_method='POST')
def monitoredSite_newLocation(request, _id = None):

	print ('new Location')	
	
	if (_id != None) :
		location = request['location']
	else :
		location = request.json_body

	print(_id)
	new_location = MonitoredSitePosition(site = location['site'], lat = location['lat'], lon = location['lon'], ele = location['ele']
		, precision= location['precision'], date = func.now() , begin_date = location['begin_date'] 
		, end_date = location['end_date'], comments = location['comments'])
	DBSession.add(new_location)
	DBSession.flush()

	location['id'] = new_location.id
	if (_id != None) :
		request['location'] = location
		return request
	else :
		return location
