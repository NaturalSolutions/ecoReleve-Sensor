"""
Created on Mon Sep  1 17:28:02 2014

@author: Natural Solutions (Thomas)
"""

from pyramid.view import view_config
from sqlalchemy import select, distinct, join, and_, desc
from ecorelevesensor.models import DBSession, MonitoredSite, MonitoredSitePosition
prefix = 'monitoredSite'

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
		return [dict(site) for site in data]


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
