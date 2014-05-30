from collections import OrderedDict

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from sqlalchemy import func, cast, Date, String, desc, select, create_engine, text, union, and_
from sqlalchemy.sql.expression import label

from pyramid.httpexceptions import HTTPBadRequest

import datetime

from .models import (
    DBSession,
    Argos,
    Gps,
    Birds,
    Sat_Trx
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
   
   try:
      ptt = int(request.GET['id'])
   except:
      raise HTTPBadRequest()

   # Get all unchecked data for this ptt
   argos_data = select([Argos.date.label('date'), cast(Argos.lat, String).label('lat'), cast(Argos.lon, String).label('lon'), 0]).where(and_(Argos.checked == False, Argos.ptt == ptt))
   gps_data = select([Gps.date.label('date'), cast(Gps.lat, String).label('lat'), cast(Gps.lon, String).label('lon'), 1]).where(and_(Gps.checked == False, Gps.ptt == ptt))
   all_data = union(argos_data, gps_data)

   # Get information for this ptt
   ptt_infos = select([Sat_Trx.ptt, Sat_Trx.manufacturer, Sat_Trx.model]).where(Sat_Trx.ptt == ptt)

   # Initialize json object
   data = {'ptt':{}, 'locations':[], 'bird':{}}
   
   # Type 0 = Argos data, type 1 = GPS data
   for date, lat, lon, type in DBSession.execute(all_data.order_by(desc(all_data.c.date))).fetchall():
      data['locations'].append({'type':type, 'date':date, 'lat':lat, 'lon':lon})
   
   try:
      data['ptt'].ptt, data['ptt'].manufacturer, data['ptt'].model = DBSession.execute(ptt_infos).fetchone()
   except TypeError:
      data['ptt'] = {}
   
   return data

@view_config(route_name='unchecked_summary', renderer='json')
def uncheckedSummary(request):
   # Initialize json object
   data = OrderedDict()
   # SQL query
   unchecked = union(
                  select([Argos.id.label('id'), Argos.ptt.label('ptt')]).where(Argos.checked == 0),
                  select([Gps.id.label('id'), Gps.ptt.label('ptt')]).where(Gps.checked == 0)
               ).alias()
   # Sum GPS and Argos locations for each ptt.
   count_by_ptt = select([unchecked.c.ptt, func.count().label('nb')]).group_by(unchecked.c.ptt).alias()
   # Add the bird associated to each ptt.
   unchecked_data = DBSession.execute(select([count_by_ptt.c.ptt, count_by_ptt.c.nb, Birds.id.label('ind_id')]).select_from(count_by_ptt.outerjoin(Birds, count_by_ptt.c.ptt == Birds.ptt)).order_by(count_by_ptt.c.ptt))
   # Populate Json object
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