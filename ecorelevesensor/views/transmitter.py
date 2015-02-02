"""
Created on Thu Sep 11 14:41:48 2014

@author: Natural Solutions (Thomas)
"""

from collections import OrderedDict

from pyramid.view import view_config
from sqlalchemy import select

from ecorelevesensor.models import DBSession
from ecorelevesensor.models.object import ObjectGsm

route_prefix = 'transmitter/'

@view_config(route_name=route_prefix + 'search/values', renderer='json')
def transmitter_values(request):
    ''' Get the different values of the field_name given in parameter.
        If a parameter limit is passed, then limit the number of values returned.
    '''
    column = request.params['field_name']
    limit  = int(request.params.get('limit', 0))
    if column in ObjectGsm.__table__.columns:
        query = select([ObjectGsm.__table__.c[column]]
            ).where(ObjectGsm.__table__.columns[column]!=None
            ).order_by(ObjectGsm.__table__.columns[column]
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
    query = select(ObjectGsm.__table__.c)
    # Look over the criteria list
    criteria = request.json_body.get('criteria', {})
    for column, value in criteria.items():
        if column in ObjectGsm.__table__.c and value != '':
            query = query.where(ObjectGsm.__table__.c[column] == value)
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
        if column in ObjectGsm.__table__.columns:
            if order == 'asc':
                order_by_clause.append(ObjectGsm.__table__.columns[column].asc())
            elif order == 'desc':
                order_by_clause.append(ObjectGsm.__table__.columns[column].desc())
    if len(order_by_clause) > 0:
        query = query.order_by(*order_by_clause)
    # Run query
    return [OrderedDict(row) for row in DBSession.execute(query).fetchall()]



@view_config(route_name=route_prefix + 'export', renderer='csv', request_method='POST')
def core_individuals_export(request):

    query = select(ObjectGsm.__table__.c)
    # Look over the criteria list
    criteria = request.json_body.get('criteria', {})
    for column, value in criteria.items():
        if column in ObjectGsm.__table__.c and value != '':
            query = query.where(ObjectGsm.__table__.c[column] == value)

    # Run query
    data = DBSession.execute(query).fetchall()
    header = [col.name for col in ObjectGsm.__table__.c]
    rows = [[val for val in row] for row in data]
    
    # override attributes of response
    filename = 'object_search_export.csv'
    request.response.content_disposition = 'attachment;filename=' + filename
    
    return {
        'header': header,
        'rows': rows,
    }
