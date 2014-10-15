from datetime import datetime
from decimal import Decimal
from urllib.parse import quote_plus
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.request import Request, Response
from pyramid.renderers import JSON
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from ecorelevesensor.controllers.security import SecurityRoot, role_loader
from ecorelevesensor.renderers.csvrenderer import CSVRenderer
from ecorelevesensor.renderers.pdfrenderer import PDFrenderer
from ecorelevesensor.renderers.gpxrenderer import GPXRenderer
from ecorelevesensor.models import (
   DBSession,
   Base,
   dbConfig
)

# Define a new request factory allowing cross-domain AJAX calls.
def request_factory(env):
	request = Request(env)
	request.response = Response()
	request.response.headerlist.extend([('Access-Control-Allow-Origin', '*')])
	return request

def datetime_adapter(obj, request):
    """Json adapter for datetime objects.
    """
    return str(obj)
    
def decimal_adapter(obj, request):
    """Json adapter for Decimal objects.
    """
    return float(obj)

# Add all the routes of the application.
def add_routes(config):
    config.add_route('weekData', 'ecoReleve-Sensor/weekData')
    
    ##### Security routes #####
    config.add_route('security/login', 'ecoReleve-Core/security/login')
    config.add_route('security/logout', 'ecoReleve-Core/security/logout')
    config.add_route('security/has_access', 'ecoReleve-Core/security/has_access')
    
    ##### User #####
    config.add_route('core/user', 'ecoReleve-Core/user')
    config.add_route('core/currentUser', 'ecoReleve-Core/currentUser')
    
    ##### Argos #####
    config.add_route('sensor/unchecked', 'ecoReleve-Sensor/sensor/unchecked')
    config.add_route('argos/unchecked/list', 'ecoReleve-Sensor/argos/unchecked/list')
    config.add_route('argos/unchecked/count', 'ecoReleve-Sensor/argos/unchecked/count')
    config.add_route('argos/unchecked', 'ecoReleve-Sensor/argos/unchecked')
    config.add_route('argos/check', 'ecoReleve-Sensor/argos/check')
    config.add_route('argos/insert', 'ecoReleve-Sensor/argos/insert')

    config.add_route('gps/unchecked/count', 'ecoReleve-Sensor/gps/unchecked/count')

    ##### RFID #####
    config.add_route('rfid', 'ecoReleve-Core/rfid')
    config.add_route('rfid/identifier', 'ecoReleve-Core/rfid/identifier')
    config.add_route('rfid/import', 'ecoReleve-Core/rfid/import')
    config.add_route('rfid/validate', 'ecoReleve-Core/rfid/validate')
    config.add_route('rfid/byName', 'ecoReleve-Core/rfid/byName/{name}')
    
    ##### GSM #####
    config.add_route('dataGsm/unchecked/list', 'ecoReleve-Core/dataGsm/unchecked/list')
    config.add_route('dataGsm/unchecked/import', 'ecoReleve-Core/dataGsm/{id}/unchecked/import')
    config.add_route('dataGsm/unchecked', 'ecoReleve-Core/dataGsm/{id}/unchecked')
    
     ##### Transmitter #####
    config.add_route('transmitter/search/values', 'ecoReleve-Core/transmitter/search/values')
    config.add_route('transmitter/search', 'ecoReleve-Core/transmitter/search')
    
    ##### Monitored sites #####
    config.add_route('monitoredSite/name', 'ecoReleve-Core/monitoredSite/name')
    config.add_route('monitoredSite/type', 'ecoReleve-Core/monitoredSite/type')
    config.add_route('monitoredSite', 'ecoReleve-Core/monitoredSite')
    config.add_route('monitoredSite/id', 'ecoReleve-Core/monitoredSite/{id}')
    config.add_route('monitoredSite/list', 'ecoReleve-Core/monitoredSite/list')
    
    ##### Stations #####
    config.add_route('station/id', 'ecoReleve-Core/station/{id}')
    config.add_route('station', 'ecoReleve-Core/station')

     ##### Monitored sites equipment #####
    config.add_route('monitoredSiteEquipment/pose', 'ecoReleve-Core/monitoredSiteEquipment/pose')
    
    config.add_route('station_graph', 'ecoReleve-Core/stations/graph')

    config.add_route('theme/list', 'ecoReleve-Core/theme/list')
    
    ##### Individuals routes #####
    config.add_route('core/individual', 'ecoReleve-Core/individual/{id}')
    config.add_route('core/individuals/history', 'ecoReleve-Core/individuals/history')
    config.add_route('core/individuals/stations', 'ecoReleve-Core/individuals/stations')
    config.add_route('core/individuals/search/values', 'ecoReleve-Core/individuals/search/values')
    config.add_route('core/individuals/search', 'ecoReleve-Core/individuals/search')
    config.add_route('core/individuals/search/export', 'ecoReleve-Core/individuals/search/export')
    config.add_route('core/individuals/count', 'ecoReleve-Core/individuals/count')

    config.add_route('core/user/fieldworkers','ecoReleve-Core/user/fieldworkers')
    config.add_route('core/protocoles/list','ecoReleve-Core/protocoles/list')
    config.add_route('core/views/list','ecoReleve-Core/views/list')
    config.add_route('core/views/export/details','ecoReleve-Core/views/details/{name}')
    config.add_route('core/views/export/count', 'ecoReleve-Core/views/{name}/count')
    config.add_route('core/views/export/filter/count', 'ecoReleve-Core/views/filter/{name}/count')
    config.add_route('core/views/export/filter/geo', 'ecoReleve-Core/views/filter/{name}/geo')
    config.add_route('core/views/export/filter/result', 'ecoReleve-Core/views/filter/{name}/result')
    config.add_route('core/views/export/filter/export', 'ecoReleve-Core/views/filter/{name}/export')

    ##### Autocomplete routes #####
    config.add_route('core/autocomplete', 'ecoReleve-Core/autocomplete')
    config.add_route('rifd_monitored_add', 'ecoReleve-Sensor/rifd_monitored/add')
   
    ##### Map routes #####
    config.add_route('map/add', 'ecoReleve-Sensor/map/add/{name}')
    config.add_route('map/create', 'ecoReleve-Sensor/map/create/{name}')
    config.add_route('map/closest_to', 'ecoReleve-Sensor/map/{name}/closest_to')
    config.add_route('map/drop', 'ecoReleve-Sensor/map/drop/{name}')

def add_views(config):
   config.add_view('ecorelevesensor.views.map.create', route_name='map/create')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['sqlalchemy.url'] = settings['cn.dialect'] + quote_plus(settings['sqlalchemy.url'])
    engine = engine_from_config(settings, 'sqlalchemy.')
    dbConfig['data_schema'] = settings['data_schema']
    dbConfig['sensor_schema'] = settings['sensor_schema']
    dbConfig['url'] = settings['sqlalchemy.url']
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    Base.metadata.reflect(views=True, extend_existing=False)
    authn_policy = AuthTktAuthenticationPolicy(
        settings['auth.secret'],
        cookie_name='ecoReleve-Core',
        callback=role_loader,
        hashalg='sha512',
        max_age=86400)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings)
    
    # Add renderer for datetime objects
    json_renderer = JSON()
    json_renderer.add_adapter(datetime, datetime_adapter)
    json_renderer.add_adapter(Decimal, decimal_adapter)
    config.add_renderer('json', json_renderer)
    
    # Add renderer for CSV files.
    config.add_renderer('csv', CSVRenderer)
    config.add_renderer('pdf', PDFrenderer)
    config.add_renderer('gpx', GPXRenderer)
    
    # Set up authentication and authorization
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(SecurityRoot)
    # Set the default permission level to 'read'
    config.set_default_permission('read')
    
    config.include('pyramid_tm')
    #config.set_request_factory(request_factory)
    add_routes(config)
    #add_views(config)
    config.scan()
    return config.make_wsgi_app()
