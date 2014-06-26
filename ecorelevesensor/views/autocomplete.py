from sqlalchemy import text
from ecorelevesensor.models import DBSession, data_schema
from pyramid.view import view_config

@view_config(route_name='core/autocomplete', renderer='json')
def autocomplete(request):
   try:
      table_name = '.'.join([data_schema, request.params['table_name']])
      column_name = request.params['column_name']
      query = text('select distinct {column} from {table}'.format(column=column_name, table=table_name))
      return [item[0] for item in DBSession.execute(query).fetchall()]
   except:
      return []