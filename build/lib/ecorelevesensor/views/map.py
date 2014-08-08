from pyramid.view import view_config
from ecorelevesensor.models import DBSession
from sqlalchemy import Table, MetaData, text, insert, String, Column
from ecorelevesensor.models import Base
from ecorelevesensor.models.temp import spatial_table
from pyramid.httpexceptions import HTTPCreated, HTTPOk, HTTPInternalServerError

schema = 'ecoReleve_Spatial.dbo'
srid = 4326

@view_config(route_name='map/create')
def map_create(request):
   name = request.matchdict['name']
   fullName = schema + name
   DBSession.execute('create table ' + fullName + ' (id INTEGER NOT NULL Identity(1,1) PRIMARY KEY, geo geometry NULL); create spatial index Idx_Spatial_' +
                     name + ' on ' + fullName + '(geo) WITH ( BOUNDING_BOX = (-180, -90, 180, 90) )')
   return HTTPCreated()

@view_config(route_name = 'map/add', request_method = ['POST'])
def map_add(request):
   points = request.json_body
   name = request.matchdict['name']
   geoms = [{'geo':'POINT(' + point['lat'] + ', ' + point['lon'] + ', ' + srid + ')'} for point in points]
   Base.metadata.reflect(schema = schema, only = [name])
   DBSession.execute(Base.metadata.tables['.'.join([schema, name])].insert(), geoms)
   return HTTPOk()

@view_config(route_name='map/drop')
def map_drop(request):
   DBSession.execute('drop table ' + db + request.matchdict['name'] + ' ;')
   return HTTPOk()

@view_config(route_name = 'map/closest_to', renderer = 'json')
def map_add(request):
   name = request.matchdict['name']
   table = '.'.join([schema, name])
   point = "geo.STDistance(geometry::Point({lat}, {lon}, {srid}))".format(lon=request.params['lon'], lat=request.params['lat'], srid=srid)
   tol = float(request.params['tol'])
   id, dist = DBSession.execute(text('select TOP 1 id, {point} from {table} where {point} is not null and {point} < :tol order by {point} asc'.format(point=point, table=table)), {'tol':tol}).fetchone()
   return {'id':id, 'dist':dist}