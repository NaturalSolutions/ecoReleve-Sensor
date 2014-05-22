from collections import OrderedDict

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from sqlalchemy import func, cast, Date, String, desc, select, create_engine, text

import datetime

from .models import (
    DBSession,
    Argos,
    Gps
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
	data = {
		'label':[str(datetime.date.today() - datetime.timedelta(days = i)) for i in range(1,8)],
		'nbArgos': [0] * 7,
		'nbGPS': [0] * 7
	}
	argos_query = DBSession.query(cast(Argos.date, Date).label('date'), func.count(Argos.id).label('nb')).filter(Argos.date >= datetime.date.today() - datetime.timedelta(days = 7)).group_by(cast(Argos.date, Date))
	gps_query = DBSession.query(cast(Gps.date, Date).label('date'), func.count(Gps.id).label('nb')).filter(Gps.date >= datetime.date.today() - datetime.timedelta(days = 7)).group_by(cast(Gps.date, Date))
	for date, nb in argos_query.all():
		try:
			i = data['label'].index(str(date))
			data['nbArgos'][i] = nb
		except:
			pass
	for date, nb in gps_query.all():
		try:
			i = data['label'].index(str(date))
			data['nbGPS'][i] = nb
		except:
			pass
	return data

engine = create_engine('mssql+pyodbc://eReleveApplication:123456@localhost\SQLSERVER2008/ecoReleve_Sensor')
DBConnection = engine.connect()

@view_config(route_name='weekDataRawSQL', renderer='json')
def weekDataRawSQL(request):
	data = {
		'label':[str(datetime.date.today() - datetime.timedelta(days = i)) for i in range(1,8)],
		'nbArgos': [0] * 7,
		'nbGPS': [0] * 7
	}
	argos_query = DBConnection.execute(text('select cast(date as DATE) as date, count(*) as nb from Targos where date >=:date group by cast(date as DATE)'), date = str(datetime.date.today() - datetime.timedelta(days = 7)))
	for date, nb in argos_query.fetchall():
		try:
			i = data['label'].index(str(date))
			data['nbArgos'][i] = nb
		except:
			pass
	gps_query = DBConnection.execute(text('select cast(date as DATE) as date, count(*) as nb from Targos where date >=:date group by cast(date as DATE)'), date = str(datetime.date.today() - datetime.timedelta(days = 7)))
	for date, nb in gps_query.fetchall():
		try:
			i = data['label'].index(str(date))
			data['nbGPS'][i] = nb
		except:
			pass
	return data

@view_config(route_name='unchecked', renderer='json')
def uncheckedData(request):
	# Get all unchecked data
	argos_data = DBSession.query(Argos.ptt, Argos.date, cast(Argos.lat, String).label('lat'), cast(Argos.lon, String).label('lon')).filter(Argos.checked == False).order_by(Argos.ptt, desc(Argos.date))
	gps_data = DBSession.query(Gps.ptt, Gps.date, cast(Gps.lat, String).label('lat'), cast(Gps.lon, String).label('lon')).filter(Gps.checked == False).order_by(Gps.ptt, desc(Gps.date))

	# Get all ptts with unchecked data
	argos_ptt = DBSession.query(Argos.ptt.label('ptt')).filter(Argos.checked == False)
	gps_ptt = DBSession.query(Gps.ptt.label('ptt')).filter(Gps.checked == False)
	ptts = argos_ptt.union(gps_ptt).order_by('ptt').distinct()

	# Initialize json object
	data = OrderedDict()
	for row in ptts:
		data[str(row.ptt)] = []
	
	# Type 0 = Argos data
	for ptt, date, lat, lon in argos_data:
		data[str(ptt)].append({'type':0, 'date':str(date), 'lat':lat, 'lon':lon})
	
	# Type 1 = Gps data
	for ptt, date, lat, lon in gps_data:
		data[str(ptt)].append({'type':1, 'date':str(date), 'lat':lat, 'lon':lon})
	
	return data