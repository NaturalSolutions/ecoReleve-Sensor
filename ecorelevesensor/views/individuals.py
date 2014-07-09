from sqlalchemy import select, cast, Date, Float, desc, join
from ecorelevesensor.models import DBSession
from ecorelevesensor.models.data import (
   CaracTypes,
   V_Search_Indiv,
   V_Individuals_LatLonDate,
   V_Individuals_History
)
from pyramid.view import view_config
from collections import OrderedDict
from datetime import datetime

route_prefix = 'core/individuals/'

@view_config(route_name=route_prefix + 'search/values', renderer='json')
def core_individuals_values(request):
   ''' Get the different values of the field_name given in parameter.
       If a parameter limit is passed, then limit the number of values returned.
   '''
   try:
      column = request.params['field_name']
      limit  = int(request.params.get('limit', 0))
      if column in V_Search_Indiv.columns:
         query = select([V_Search_Indiv.columns[column]]).where(V_Search_Indiv.columns[column]!=None).order_by(V_Search_Indiv.columns[column]).distinct()
         if limit > 0:
            query = query.limit(limit)
         return [item[column] for item in DBSession.execute(query).fetchall()]
      else:
         return []
   except:
      return []

@view_config(route_name=route_prefix + 'search', renderer='json', request_method='POST')
def core_individuals_search(request):
   ''' Search individuals by posting a JSON object containing the fields :
      - criteria : dict object with column_name:value fields
      - order_by : dict object with column_name:'asc' or column_name:'desc' fields
      - offset   : int
      - limit    : int
   '''
   try:
      query = select(V_Search_Indiv.c)
      # Look over the criteria list
      criteria = request.json_body.get('criteria', {})
      for column, value in criteria.items():
         if column in V_Search_Indiv.columns:
            query = query.where(V_Search_Indiv.columns[column] == value)
      # Define the limit and offset if exist
      limit = int(request.json_body.get('limit', 0))
      offset = int(request.json_body.get('offset', 0))
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
         result.append(OrderedDict(row))
      return result
   except:
      return []

@view_config(route_name=route_prefix + 'stations', renderer='json')
def core_individuals_stations(request):
   ''' Get the stations of an identified individual. Parameter is : id (int)'''
   try:
      id = int(request.params['id'])
      # Query
      query = select([cast(V_Individuals_LatLonDate.c.lat, Float), cast(V_Individuals_LatLonDate.c.lon, Float), V_Individuals_LatLonDate.c.date]
                     ).where(V_Individuals_LatLonDate.c.indID == id).order_by(V_Individuals_LatLonDate.c.date)
      # Create list of features from query result
      features = [{'type':'Feature', 'properties':{'date':int((date-datetime.utcfromtimestamp(0)).total_seconds())}, 'geometry':{'type':'Point', 'coordinates':[lon,lat]}}
                  for lat, lon, date in DBSession.execute(query).fetchall()]
      result = {'type':'FeatureCollection', 'features':features}
      return result
   except:
      return []

@view_config(route_name=route_prefix + 'history', renderer='json')
def core_individuals_history(request):
   ''' Get the history of an identified individual. Parameter is : id (int)'''
   try:
      id = int(request.params['id'])
      # Query for characteristic history list
      query = select([V_Individuals_History.c.label, V_Individuals_History.c.value, cast(V_Individuals_History.c.begin_date, Date), cast(V_Individuals_History.c.end_date, Date)]
                     ).where(V_Individuals_History.c.id == id
                     ).order_by(V_Individuals_History.c.carac, desc(V_Individuals_History.c.begin_date))
      # Create list of characteristic history
      null_date_filter = lambda date: str(date) if date is not None else date
      history = [OrderedDict([('characteristic',label), ('value',value), ('from',str(begin_date)), ('to',null_date_filter(end_date))]) for label, value, begin_date, end_date in DBSession.execute(query).fetchall()]
      result = {'history':history}
      # Get current value from the list, preventing a new connection to the database
      result['Age'] = next((item['value'] for item in history if item['characteristic'] == 'Age'), None)
      result['PTT'] = next((item['value'] for item in history if item['characteristic'] == 'PTT'), None)
      result['Origin'] = next((item['value'] for item in history if item['characteristic'] == 'Origin'), None)
      return result
   except:
      return []