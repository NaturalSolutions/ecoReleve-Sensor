"""
Created on Fri Sep 19 17:24:09 2014

@author: Natural Solutions (Thomas)
"""

from pyramid.view import view_config
from sqlalchemy import select, distinct, join, text,Table
from ecorelevesensor.models import DBSession, Station,Base
import numpy as np

prefix = 'station'

@view_config(route_name=prefix, renderer='json', request_method='GET')
def monitoredSites(request):
   
	data = DBSession.query(Station).all()
	return data

@view_config(route_name=prefix+'/id', renderer='json', request_method='GET')
def monitoredSite(request):
   
	id_ = request.matchdict['id']
	print ('___________________________________ ID \n')
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
def monitoredSites(request):
	
	proto_view_Name=request.matchdict['name_vue']
	proto_view_Table=Base.metadata.tables[proto_view_Name]
	join_table=proto_view_Table.join(Station, proto_view_Table.c['TSta_PK_ID'] == Station.id )
	
	slct=select([Station.locality]).distinct().select_from(join_table)
	data = DBSession.execute(slct).fetchall()

	return [row['Place' or 'Locality'] for row in data]