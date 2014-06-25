from collections import OrderedDict
from array import array
from geopy.distance import vincenty

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from sqlalchemy import func, cast, Date, String, desc, select, create_engine, text, union, and_, insert, bindparam, Sequence, update, or_, literal_column
from sqlalchemy.sql.expression import label

from pyramid.httpexceptions import HTTPBadRequest, HTTPCreated, HTTPServerError, HTTPOk

import datetime, operator

from ecorelevesensor.models import DBSession

from ecorelevesensor.models.sensor import Argos, Gps
from ecorelevesensor.models.data import (
   Individuals,
   ProtocolArgos,
   ProtocolGps,
   ProtocolIndividualEquipment,
   SatTrx,
   Station
   )

# Data imported from the CLS WS during the last week.
@view_config(route_name='weekData', renderer='json')
def weekData(request):
   # Initialize Json object
   data = {
      'label':[str(datetime.date.today() - datetime.timedelta(days = i)) for i in range(1,8)],
      'nbArgos': [0] * 7,
      'nbGPS': [0] * 7
   }

   # Argos data
   argos_query = select([cast(Argos.date, Date).label('date'), func.count(Argos.id).label('nb')]).where(Argos.date >= datetime.date.today() - datetime.timedelta(days = 7)).group_by(cast(Argos.date, Date))
   for date, nb in DBSession.execute(argos_query).fetchall():
      try:
         i = data['label'].index(str(date))
         data['nbArgos'][i] = nb
      except:
         pass

   # GPS data
   gps_query = select([cast(Gps.date, Date).label('date'), func.count(Gps.id).label('nb')]).where(Gps.date >= datetime.date.today() - datetime.timedelta(days = 7)).group_by(cast(Gps.date, Date))
   for date, nb in DBSession.execute(gps_query).fetchall():
      try:
         i = data['label'].index(str(date))
         data['nbGPS'][i] = nb
      except:
         pass
   
   return data

# Unchecked data for one PTT.
@view_config(route_name='argos/unchecked', renderer='json')
def argos_unchecked(request):
   
   # ptt is a mandatory parameter.
   try:
      ptt = int(request.GET['ptt'])
   except:
      raise HTTPBadRequest()

   # Get all unchecked data for this ptt and this individual
   argos_data = select([Argos.id.label('id'), Argos.date.label('date'), cast(Argos.lat, String).label('lat'), cast(Argos.lon, String).label('lon'), Argos.lc.label('lc'), literal_column('0').label('type')]
                       ).where(and_(Argos.checked == False, Argos.ptt == ptt))
   gps_data = select([Gps.id.label('id'), Gps.date.label('date'), cast(Gps.lat, String).label('lat'), cast(Gps.lon, String).label('lon'), literal_column('NULL').label('lc'),literal_column('1').label('type')]
                     ).where(and_(Gps.checked == False, Gps.ptt == ptt))
   unchecked = union(argos_data, gps_data).alias('unchecked')

   # ind_id is a facultative parameter
   try:
      ind_id = int(request.GET['ind_id'])
      all_data = select([unchecked.c.id, unchecked.c.date, unchecked.c.lat, unchecked.c.lon, unchecked.c.lc, unchecked.c.type]).select_from(
         unchecked.join(SatTrx, SatTrx.ptt == ptt).join(ProtocolIndividualEquipment, and_(
            SatTrx.id == ProtocolIndividualEquipment.sat_id, unchecked.c.date >= ProtocolIndividualEquipment.begin_date, or_(
               unchecked.c.date < ProtocolIndividualEquipment.end_date, ProtocolIndividualEquipment.end_date == None
               )
            )
         )
      ).where(
         ProtocolIndividualEquipment.ind_id == ind_id
      )
   except KeyError, TypeError:
      all_data = select([unchecked.c.id, unchecked.c.date, unchecked.c.lat, unchecked.c.lon, unchecked.c.lc, unchecked.c.type])
      ind_id = None

   # Initialize json object
   data = {'ptt':{}, 'locations':[], 'indiv':{}}
   
   # Type 0 = Argos data, type 1 = GPS data
   for id, date, lat, lon, lc, type in DBSession.execute(all_data.order_by(desc('date'))).fetchall():
      data['locations'].append({'id': id, 'type':type, 'date':str(date), 'lat':lat, 'lon':lon, 'lc':lc, 'dist':0})
      try:
         # Distance from last location
         data['locations'][-2]['dist'] = round(vincenty((data['locations'][-2]['lat'], data['locations'][-2]['lon']), (data['locations'][-1]['lat'], data['locations'][-1]['lon'])).kilometers, 3)
      except IndexError:
         pass
      
   # Get informations for this ptt
   ptt_infos = select([SatTrx.ptt, SatTrx.manufacturer, SatTrx.model]).where(SatTrx.ptt == ptt)
   data['ptt']['ptt'], data['ptt']['manufacturer'], data['ptt']['model'] = DBSession.execute(ptt_infos).fetchone()

   # Get informations for the individual
   if ind_id is not None:
      indiv_infos = select([Individuals.id, Individuals.age, Individuals.sex, Individuals.specie, Individuals.monitoring_status, Individuals.origin, Individuals.survey_type]).where(Individuals.id == ind_id)
      data['indiv']['id'], data['indiv']['age'], data['indiv']['sex'], data['indiv']['specie'], data['indiv']['monitoring_status'], data['indiv']['origin'], data['indiv']['survey_type'] = DBSession.execute(indiv_infos).fetchone()
      # Last known location
      data['indiv']['last_loc'] = {}
      last_loc = data['indiv']['last_loc']
      query = 'select convert(varchar, StaDate, 120), convert(float, LAT), convert(float, LON) from ecoReleve_Data.dbo.fn_v_qry_GetMaxStation(:ind_id)'
      last_loc['date'], last_loc['lat'], last_loc['lon'] = DBSession.execute(text(query), {'ind_id':ind_id}).fetchone()

   return data

# List all PTTs having unchecked locations, with individual id and number of locations.
@view_config(route_name='argos/unchecked/list', renderer='json')
def argos_unchecked_list(request):
   # Initialize Json array
   data = []
   # SQL query
   unchecked = union(select([Argos.id.label('id'), Argos.ptt.label('ptt'), Argos.date.label('date')]).where(Argos.checked == 0),
                  select([Gps.id.label('id'), Gps.ptt.label('ptt'), Gps.date.label('date')]).where(Gps.checked == 0)).alias()
   # Add the bird associated to each ptt.
   unchecked_with_ind = select([ProtocolIndividualEquipment.ind_id.label('ind_id'), 'ptt', func.count('id').label('nb')]).select_from(
      unchecked.join(SatTrx, SatTrx.ptt == unchecked.c.ptt).outerjoin(
      ProtocolIndividualEquipment, and_(SatTrx.id == ProtocolIndividualEquipment.sat_id, unchecked.c.date >= ProtocolIndividualEquipment.begin_date, or_(unchecked.c.date < ProtocolIndividualEquipment.end_date, ProtocolIndividualEquipment.end_date == None)))
      ).group_by('ptt', ProtocolIndividualEquipment.ind_id).order_by('ptt')
   # Populate Json array
   for ind_id, ptt, nb in DBSession.execute(unchecked_with_ind).fetchall():
      data.append({'ptt':ptt,'ind_id':ind_id, 'count':nb})
   return data

# Count the number of unchecked data.
@view_config(route_name = 'argos/unchecked/count', renderer = 'json')
def argos_unchecked_count(request):
   return DBSession.execute(select([func.count(Argos.id)]).where(Argos.checked == 0)).scalar()

@view_config(route_name = 'argos/insert', renderer = 'json')
def argos_insert(request):
   stations = []
   argos_id = array('i')
   gps_id = array('i')

   # Query that check for duplicate stations
   check_duplicate_station = select([func.count(Station.id)]).where(and_(Station.name == bindparam('name'), Station.lat == bindparam('lat'), Station.lon == bindparam('lon'), Station.ele == bindparam('ele')))
   
   # For each objet in the request body
   for ptt_obj in request.json_body:
      ptt = ptt_obj['ptt']
      ind_id = ptt_obj['ind_id']
         
      # For each location associated with this object
      for location in ptt_obj['locations']:
         # Argos
         if location['type'] == 0:
            # Get all the informations about the sensor data
            argos_data = DBSession.query(Argos).filter_by(id=location['id']).one()
            name = 'ARGOS_' + str(argos_data.ptt) + '_' + argos_data.date.strftime('%Y%m%d%H%M%S')
            if DBSession.execute(check_duplicate_station, {'name':name, 'lat':argos_data.lat, 'lon':argos_data.lon, 'ele':argos_data.ele}).scalar() == 0:
               argos = ProtocolArgos(ind_id=ind_id, lc=argos_data.lc, iq=argos_data.iq, nbMsg=argos_data.nbMsg, nbMsg120=argos_data.nbMsg120,
                                       bestLvl=argos_data.bestLvl, passDuration=argos_data.passDuration, nopc=argos_data.nopc, frequency=argos_data.frequency)
               station = Station(date=argos_data.date, name=name, fieldActivityId=27, fieldActivityName='Argos', lat=argos_data.lat, lon=argos_data.lon, ele=argos_data.ele, protocol_argos=argos)
               # Add the station in the list
               argos_id.append(location['id'])
               stations.append(station)
         # Gps
         elif location['type'] == 1:
            gps_data = DBSession.query(Gps).filter_by(id=location['id']).one()
            name = 'ARGOS_' + str(gps_data.ptt) + '_' + gps_data.date.strftime('%Y%m%d%H%M%S')
            if DBSession.execute(check_duplicate_station, {'name':name, 'lat':argos_data.lat, 'lon':argos_data.lon, 'ele':argos_data.ele}).scalar() == 0:    
               gps = ProtocolGps(ind_id=ind_id, course=gps_data.course, speed=gps_data.speed)
               station = Station(date=argos_data.date, name=name, fieldActivityId=27, fieldActivityName='Argos', lat=argos_data.lat, lon=argos_data.lon, ele=argos_data.ele, protocol_gps=gps)
               # Add the station in the list
               gps_id.append(location['id'])
               stations.append(station)
   # Insert the stations (and protocols thanks to ORM)
   DBSession.add_all(stations)
   # Update the sensor database
   DBSession.execute(update(Argos).where(Argos.id.in_(argos_id)).values(checked=True, imported=True))
   DBSession.execute(update(Gps).where(Gps.id.in_(gps_id)).values(checked=True, imported=True))
   return {'status':'ok'}

@view_config(route_name = 'argos/check', renderer = 'json')
def argos_check(request):
   argos_id = array('i')
   gps_id = array('i')
   try:
      for ptt_obj in request.json_body:
         ptt = ptt_obj['ptt']
         ind_id = ptt_obj['ind_id']
         for location in ptt_obj['locations']:
            if location['type'] == 0:
               argos_id.append(location['id'])
            elif location['type'] == 1:
               gps_id.append(location['id'])
      DBSession.execute(update(Argos).where(Argos.id.in_(argos_id)).values(checked=True))
      DBSession.execute(update(Gps).where(Gps.id.in_(gps_id)).values(checked=True))
      return {'argosChecked': len(argos_id), 'gpsChecked':len(gps_id)}
   except Exception as e:
      raise

@view_config(route_name = 'station_graph', renderer = 'json')
def station_graph(request):
   # Initialize Json object
   data = OrderedDict()

   # Calculate the bounds
   today = datetime.date.today()
   begin_date = datetime.date(day = 1, month = today.month, year = today.year - 1)
   end_date = datetime.date(day = 1, month = today.month, year = today.year)

   # Query
   query = select([func.count(Station.id).label('nb'), func.year(Station.date).label('year'), func.month(Station.date).label('month')]
                  ).where(and_(Station.date >= begin_date, Station.date < end_date)).group_by(func.year(Station.date), func.month(Station.date))

   # Execute query and sort result by year, month (faster than an order_by clause in this case)
   for nb, y, m in sorted(DBSession.execute(query).fetchall(), key = operator.itemgetter(1,2)):
      data[datetime.date(day = 1, month = m, year = y).strftime('%b') + ' ' + str(y)] = nb

   return data

@view_config(route_name = 'individuals/count', renderer = 'json')
def individuals_count(request):
   return DBSession.execute(select([func.count(Individuals.id).label('nb')])).scalar()