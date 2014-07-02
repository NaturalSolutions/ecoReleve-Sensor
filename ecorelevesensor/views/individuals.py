from sqlalchemy import select
from ecorelevesensor.models import DBSession
from ecorelevesensor.models.data import V_Search_Indiv
from pyramid.view import view_config

route_prefix = 'core/individuals/'

@view_config(route_name=route_prefix + 'search/values', renderer='json')
def core_individuals_values(request):
   ''' Get the different values of the field given in parameter '''
   try:
      column = request.params['field_name']
      if column in V_Search_Indiv.columns:
         query = select([V_Search_Indiv.columns[column]]).where(V_Search_Indiv.columns[column]!=None).distinct()
         return [item[column] for item in DBSession.execute(query).fetchall()]
      else:
         return []
   except:
      return []

@view_config(route_name=route_prefix + 'search', renderer='json', request_method='POST')
def core_individuals_search(request):
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
      # Set sorting columns and order
      order_by = request.json_body.get('order_by', {})
      order_by_clause = []
      for column, order in order_by.items():
         if column in V_Search_Indiv.columns:
            if order == 'asc':
               order_by_clause.append(V_Search_Indiv.columns[column].asc())
            elif order == 'desc':
               order_by_clause.append(V_Search_Indiv.columns[column].desc())
      if len(order_by_clause) > 0:
         query = query.order_by(*order_by_clause)
      # Run query
      result = []
      for row in DBSession.execute(query).fetchall():
         result.append({column:row[column] for column in row.keys()})
      return result
   except:
      return []