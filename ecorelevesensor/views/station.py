"""
Created on Fri Sep 19 17:24:09 2014

@author: Natural Solutions (Thomas)
"""

from pyramid.view import view_config
from sqlalchemy import select, distinct, join, text
from ecorelevesensor.models import DBSession, Station

prefix = 'station'

@view_config(route_name=prefix, renderer='json', request_method='GET')
def monitoredSites(request):
    data = DBSession.query(Station).all()
    return data

@view_config(route_name=prefix+'/id', renderer='json', request_method='GET')
def monitoredSite(request):
    id_ = request.matchdict['id']
    data = DBSession.query(Station).filter(Station.id == id_).one()
    return data