from sqlalchemy import select, join
from ecorelevesensor.models import DBSession, data_schema
from ecorelevesensor.models.data import ProtocolReleaseIndividual, Individuals, Station
from pyramid.view import view_config

route_prefix = 'core/individuals/'

@view_config(route_name=route_prefix + 'released', renderer='json')
def core_individuals_stations(request):
   try:
      conditions = ''
      for key, item in request.params:
         if len(conditions) == 0:
            conditions += str(key) + '=' + str(item)
         else:
            conditions += ' ' + 'and ' + str(key) + '=' + str(item)

      query = 'select'
   except:
      raise
   return []

@view_config(route_name=route_prefix + 'released/values', renderer='json')
def core_individuals_stations(request):
   try:
      field = request.params['field_name']
      query = select([field]).select_from(join(ProtocolReleaseIndividual,Individuals).join(Station)).distinct()
      return [item[0] for item in DBSession.execute(query).fetchall()]
   except:
      raise