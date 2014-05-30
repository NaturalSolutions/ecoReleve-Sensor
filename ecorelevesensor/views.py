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

@view_config(route_name='unchecked_summary', renderer='json')
def uncheckedSummary(request):
	# Initialize json object
	data = OrderedDict()
	
	# SQL query
	unchecked_data = DBSession.execute(text("""select ptt, nb, Individual_Obj_PK as ind_id from 
   (select ptt, sum(nb) as nb from ( select FK_ptt as ptt, count(*) as nb from Targos where checked = 0 group by FK_ptt union select FK_ptt as ptt, count(*) as nb from Tgps where checked = 0 group by FK_ptt) as T group by ptt) as data
   left outer join ecoReleve_Data.dbo.TViewIndividual indivs on indivs.id19@TCarac_PTT = data.ptt order by ptt"""))
	
	for row in unchecked_data.fetchall():
		data.setdefault(row.ptt, []).append({'count':row.nb, 'ind_id':row.ind_id})
	
	return data

@view_config(route_name='uncheckedRaw', renderer='json')
def uncheckedRaw(request):
	# Initialize json object
	data = OrderedDict()
	
	# SQL query
	unchecked_data = DBSession.execute(text("""select FK_ptt as ptt, cast(date as VARCHAR) as date, cast(lat as VARCHAR) as lat, cast(lon as VARCHAR) as lon, type
		from ( select FK_ptt, date, lat, lon, 0 as type from Targos where checked = 0 union select FK_ptt, date, lat, lon, 1 as type from Tgps where checked = 0) as T order by ptt, date"""))
	
	for row in unchecked_data.fetchall():
		data.setdefault(row.ptt, []).append({'type':row.type, 'date':row.date, 'lat':row.lat, 'lon':row.lon})
	
	return data