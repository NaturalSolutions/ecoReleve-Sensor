from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from sqlalchemy import func, cast, Date

import datetime
import json

from .models import (
    DBSession,
    Argos,
    )


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(Argos.date).count()
    except DBAPIError as e:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'app'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_app_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(route_name='weekData', renderer='json')
def weekData(request):
    argos = DBSession.query(cast(Argos.date, Date), func.count(Argos.id)).filter(Argos.date >= datetime.date.today() - datetime.timedelta(days = 60)).group_by(cast(Argos.date, Date))
    #print argos.all()
    return argos.all()
#gps = DBSession.query(Argos).filter(date__gte = datetime.date.today()-datetime.timedelta(days=7))
#data = serializers.serialize('json', ArgosData)
    