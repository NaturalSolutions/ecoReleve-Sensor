from sqlalchemy import select
from ecorelevesensor.models import DBSession
from ecorelevesensor.models.data import V_Search_Indiv
from pyramid.view import view_config

route_prefix = 'core/individuals/'

@view_config(route_name=route_prefix + 'search/values', renderer='json')
def core_individuals_values(request):
   try:
      column = request.params['field_name']
      if column in V_Search_Indiv.columns:
         query = select([V_Search_Indiv.columns[column]]).distinct()
         return [item[column] for item in DBSession.execute(query).fetchall()]
      else:
         return []
   except:
      return []

@view_config(route_name=route_prefix + 'search', renderer='json', request_method='POST')
def core_individuals_stations(request):
   try:
      query = select(V_Search_Indiv.c)
      # Look over the criteria list
      criteria = request.json_body.get('criteria', {})
      for column, value in criteria.items():
         if column in V_Search_Indiv.columns:
            query = query.where(V_Search_Indiv.columns[column] == value)
      # Define the limit and offset if exist
      limit = request.json_body.get('limit', 0)
      offset = request.json_body.get('offset', 0)
      if limit > 0:
         query = query.limit(limit)
      if offset > 0:
         offset = query.offset(offset)
      # Set sorting column and order
      order_by = request.json_body.get('order_by', {})
      for column, order in order_by.items():
         if column in V_Search_Indiv.columns:
            if order == 'asc':
               query = query.order_by(V_Search_Indiv.columns[column].asc())
            elif order == 'desc':
               query = query.order_by(V_Search_Indiv.columns[column].desc())

      result = []
      for row in DBSession.execute(query).fetchall():
         result.append(
            {'id':row[V_Search_Indiv.c.id],
             'age':row[V_Search_Indiv.c.age],
             'specie':row[V_Search_Indiv.c.specie],
             'ptt':row[V_Search_Indiv.c.ptt],
             'sex':row[V_Search_Indiv.c.sex],
             'origin':row[V_Search_Indiv.c.origin],
             'monitoringStatus':row[V_Search_Indiv.c.monitoringStatus],
             'surveyType':row[V_Search_Indiv.c.surveyType],
             'releaseArea':row[V_Search_Indiv.c.releaseArea],
             'releaseYear':row[V_Search_Indiv.c.releaseYear],
             'captureArea':row[V_Search_Indiv.c.captureArea],
             'captureYear':row[V_Search_Indiv.c.captureYear]
            }
         )
      return result
   except:
      raise
      return []