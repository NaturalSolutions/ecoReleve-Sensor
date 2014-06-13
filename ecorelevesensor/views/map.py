from pyramid.view import view_config
from ecorelevesensor.models import DBSession
from sqlalchemy import Table, MetaData, text
from ecorelevesensor.models import Base
from ecorelevesensor.models.temp import spatial_table
from pyramid.httpexceptions import HTTPCreated, HTTPOk, HTTPInternalServerError

db = 'ecoReleve_Spatial.dbo.'
srid = 4326

@view_config(route_name='map/create')
def map_create(request):
   name = request.matchdict['name']
   fullName = db + name
   DBSession.execute('create table ' + fullName + ' (id INTEGER NOT NULL Identity(1,1) PRIMARY KEY, geo geometry NULL); create spatial index Idx_Spatial_' +
                     name + ' on ' + fullName + '(geo) WITH ( BOUNDING_BOX = (-180, -90, 180, 90) )')
   return HTTPCreated()

@view_config(route_name = 'map/add', request_method = 'POST')
def map_add(request):
   points = request.json_body
   name = request.matchdict['name']
   fullName = db + name
   geoms = [{'geom':''}]
   DBSession.execute()
   return HTTPOk()

@view_config(route_name='map/drop')
def map_drop(request):
   DBSession.execute('drop table ' + db + request.matchdict['name'] + ' ;')
   return HTTPOk()