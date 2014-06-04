from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.request import Request, Response
from sqlalchemy.engine import Connection

from .models import (
   DBSession,
   Base,
)

# Define a new request factory allowing cross-domain AJAX calls.
def request_factory(env):
	request = Request(env)
	request.response = Response()
	request.response.headerlist = []
	request.response.headerlist.extend([('Access-Control-Allow-Origin', '*')])
	return request


def main(global_config, **settings):
   """ This function returns a Pyramid WSGI application.
   """
   engine = engine_from_config(settings, 'sqlalchemy.')
   DBSession.configure(bind=engine)
   Base.metadata.bind = engine
   config = Configurator(settings=settings)
   config.include('pyramid_chameleon')
   # Views
   config.add_static_view('static', 'static', cache_max_age=3600)
   config.add_route('weekData', 'ecoReleve-Sensor/weekData')
   config.add_route('unchecked', 'ecoReleve-Sensor/unchecked')
   config.add_route('unchecked_summary', 'ecoReleve-Sensor/unchecked_summary')
   config.add_route('station_graph', 'ecoReleve-Core/stations/graph')
   config.add_route('individuals_count', 'ecoReleve-Core/individuals/count')
   config.add_route('argos/insert', 'ecoReleve-Sensor/argos/insert')
   config.set_request_factory(request_factory)
   config.scan()
   return config.make_wsgi_app()
