"""
Created on Mon Sep  1 17:28:02 2014

@author: Natural Solutions (Thomas)
"""

from pyramid.view import view_config
from sqlalchemy import select, distinct
from ecorelevesensor.models import DBSession, MonitoredSite
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
    data = DBSession.execute(select([MonitoredSite.name]).order_by(MonitoredSite.name)).fetchall()
    return [dict(site) for site in data]

@view_config(route_name=prefix+'/type', renderer='json')
def monitored_site(request):
    data = DBSession.execute(select([distinct(MonitoredSite.type_
        ).label('FK_type')]).order_by('FK_type')).fetchall()
    return [row[0] for row in data]