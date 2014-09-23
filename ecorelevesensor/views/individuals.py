from sqlalchemy import select, cast, Date, Float, desc, func
from ecorelevesensor.models import DBSession, Individual
from ecorelevesensor.models.data import (
   CaracTypes,
   V_Individuals_LatLonDate,
   V_Individuals_History
)

from ecorelevesensor.models.views import V_SearchIndiv

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from collections import OrderedDict
from datetime import datetime

route_prefix = 'core/individuals/'

@view_config(route_name=route_prefix + 'search/values', renderer='json')
def core_individuals_values(request):
    ''' Get the different values of the field_name given in parameter.
        If a parameter limit is passed, then limit the number of values returned.
    '''
    column = request.params['field_name']
    limit  = int(request.params.get('limit', 0))
    if column in V_SearchIndiv.columns:
        query = select([V_SearchIndiv.c[column]]
            ).where(V_SearchIndiv.columns[column]!=None
            ).order_by(V_SearchIndiv.columns[column]
            ).distinct()
        if limit > 0:
            query = query.limit(limit)
        return [str(item[column]) for item in DBSession.execute(query).fetchall()]
    else:
        return []

@view_config(route_name=route_prefix + 'search', renderer='json', request_method='POST')
def core_individuals_search(request):
    '''Search individuals by posting a JSON object containing the fields :
        - criteria : dict object with column_name:value fields
        - order_by : dict object with column_name:'asc' or column_name:'desc' fields
        - offset   : int
        - limit    : int
    '''
    query = select(V_SearchIndiv.c)
    # Look over the criteria list
    criteria = request.json_body.get('criteria', {})
    for column, value in criteria.items():
        if column in V_SearchIndiv.c and value != '':
            query = query.where(V_SearchIndiv.c[column] == value)
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
        if column in V_SearchIndiv.columns:
            if order == 'asc':
                order_by_clause.append(V_SearchIndiv.columns[column].asc())
            elif order == 'desc':
                order_by_clause.append(V_SearchIndiv.columns[column].desc())
    if len(order_by_clause) > 0:
        query = query.order_by(*order_by_clause)
    # Run query
    return [OrderedDict(row) for row in DBSession.execute(query).fetchall()]

@view_config(
    permission=NO_PERMISSION_REQUIRED,
    route_name=route_prefix + 'search/export',
    renderer='csv',
    request_method='POST'
)
def core_individuals_search_export(request):
    '''Search individuals by posting a JSON object containing the fields :
        - criteria : dict object with column_name:value fields
        - order_by : dict object with column_name:'asc' or column_name:'desc' fields
        - offset   : int
        - limit    : int
        Return search results as CSV.
    '''
    query = select(V_SearchIndiv.c)
    # Look over the criteria list
    criteria = request.json_body.get('criteria', {})
    for column, value in criteria.items():
        if column in V_SearchIndiv.c and value != '':
            query = query.where(V_SearchIndiv.c[column] == value)
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
        if column in V_SearchIndiv.columns:
            if order == 'asc':
                order_by_clause.append(V_SearchIndiv.columns[column].asc())
            elif order == 'desc':
                order_by_clause.append(V_SearchIndiv.columns[column].desc())
    if len(order_by_clause) > 0:
        query = query.order_by(*order_by_clause)
    
    # Run query
    data = DBSession.execute(query).fetchall()
    header = [col.name for col in V_SearchIndiv.c]
    rows = [[value for value in row] for row in data]
    
    # override attributes of response
    filename = 'individual_search_export.csv'
    request.response.content_disposition = 'attachment;filename=' + filename
   
    return {
        'header': header,
        'rows': rows,
    }

@view_config(route_name=route_prefix + 'stations', renderer='json')
def core_individuals_stations(request):
   ''' Get the stations of an identified individual. Parameter is : id (int)'''
   try:
      id = int(request.params['id'])
      # Query
      query = select([cast(V_Individuals_LatLonDate.c.lat, Float), cast(V_Individuals_LatLonDate.c.lon, Float), V_Individuals_LatLonDate.c.date]
                     ).where(V_Individuals_LatLonDate.c.ind_id == id).order_by(desc(V_Individuals_LatLonDate.c.date))
      # Create list of features from query result
      epoch = datetime.utcfromtimestamp(0)
      features = [
          {
              'type':'Feature',
              'properties':{'date':(date - epoch).total_seconds()},
              'geometry':{'type':'Point', 'coordinates':[lon,lat]}
          }
          for lat, lon, date in reversed(DBSession.execute(query).fetchall())]
                  
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
      null_date_filter = lambda date: None if date is None else str(date)
      history = [OrderedDict([('characteristic',label), ('value',value), ('from',str(begin_date)), ('to',null_date_filter(end_date))]) for label, value, begin_date, end_date in DBSession.execute(query).fetchall()]
      result = {'history':history}
      # Get current value from the list, preventing a new connection to the database
      result['Age'] = next((item['value'] for item in history if item['characteristic'] == 'Age'), None)
      result['Sex'] = next((item['value'] for item in history if item['characteristic'] == 'Sex'), None)
      result['PTT'] = next((item['value'] for item in history if item['characteristic'] == 'PTT'), None)
      result['Species'] = next((item['value'] for item in history if item['characteristic'] == 'Species'), None)
      result['Origin'] = next((item['value'] for item in history if item['characteristic'] == 'Origin'), None)
      return result
   except:
      return []

@view_config(route_name=(route_prefix + 'count'), renderer='json')
def core_individuals_count(request):
   return {'count':DBSession.execute(select([func.count(Individual.id).label('nb')])).scalar()}
   
@view_config(route_name='core/individual', renderer='json')
def core_individual(request):
    ''' Get the attributes of an identified individual.
    '''
    id = int(request.matchdict['id'])
    indiv = DBSession.query(Individual).filter(Individual.id==id).one()
    query = select([V_Individuals_History.c.label, V_Individuals_History.c.value, cast(V_Individuals_History.c.begin_date, Date), cast(V_Individuals_History.c.end_date, Date)]
                     ).where(V_Individuals_History.c.id == id
                     ).order_by(V_Individuals_History.c.carac, desc(V_Individuals_History.c.begin_date))
    carac = DBSession.execute(query).fetchall()
    null_date_filter = lambda date: None if date is None else str(date)
    indiv.history = [OrderedDict([('name',label), ('value',value), ('from',str(begin_date)), ('to',null_date_filter(end_date))]) for label, value, begin_date, end_date in carac]
    return indiv
