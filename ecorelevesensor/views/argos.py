from array import array

from pyramid.view import view_config

from sqlalchemy import func, desc, select, union, and_, bindparam, update, or_, literal_column

from pyramid.httpexceptions import HTTPBadRequest

import pandas as pd
import numpy as np

from ..models import DBSession
from ..models.sensor import Argos, Gps
from ..models.data import (
   Individuals,
   ProtocolArgos,
   ProtocolGps,
   ProtocolIndividualEquipment,
   SatTrx,
   Station,
   V_Individuals_LatLonDate
)
from ..utils.distance import haversine

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

# Unchecked data for one PTT.
@view_config(route_name='argos/unchecked', renderer='json')
def argos_unchecked(request):
   
   # ptt is a mandatory parameter.
   try:
      ptt = int(request.GET['ptt'])
   except:
      raise HTTPBadRequest()

   # Get all unchecked data for this ptt and this individual
   # Type 0 = Argos data, type 1 = GPS data
   argos_data = select([Argos.id.label('id'), Argos.date.label('date'), Argos.lat.label('lat'), Argos.lon.label('lon'), Argos.lc.label('lc'), literal_column('0').label('type')]
                       ).where(and_(Argos.checked == False, Argos.ptt == ptt))
   gps_data = select([Gps.id.label('id'), Gps.date.label('date'), Gps.lat.label('lat'), Gps.lon.label('lon'), literal_column('NULL').label('lc'),literal_column('1').label('type')]
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
   except KeyError or TypeError:
      all_data = select([unchecked.c.id, unchecked.c.date, unchecked.c.lat, unchecked.c.lon, unchecked.c.lc, unchecked.c.type])
      ind_id = None

   # Initialize json object
   data = {'ptt':{}, 'locations':[], 'indiv':{}}
   
   # Load data from the DB then
   # compute the distance between 2 consecutive points.
   res = DBSession.execute(all_data.order_by(desc('date'))).fetchall()
   df = pd.DataFrame.from_records(res, columns=res[0].keys(), coerce_float=True)
   X1 = df.ix[:,['lat', 'lon']].values[:-1,:]
   X2 = df.ix[1:,['lat', 'lon']].values
   dist = pd.Series(np.append(haversine(X1, X2).round(3), 0), name='dist')
   df = pd.concat([df['id'], df['date'].apply(lambda x: str(x)), df['lat'], df['lon'], df['lc'], df['type'], dist], axis=1)
   data['locations'] = df.to_dict('records')

   # Get informations for this ptt
   ptt_infos = select([SatTrx.ptt, SatTrx.manufacturer, SatTrx.model]).where(SatTrx.ptt == ptt)
   data['ptt']['ptt'], data['ptt']['manufacturer'], data['ptt']['model'] = DBSession.execute(ptt_infos).fetchone()

   # Get informations for the individual
   if ind_id is not None:
      query = select([
         Individuals.id.label('id'),
         Individuals.age.label('age'),
         Individuals.sex.label('sex'),
         Individuals.specie.label('specie'),
         Individuals.monitoring_status.label('monitoring_status'), 
         Individuals.origin.label('origin'),
         Individuals.survey_type.label('survey_type')
         ]).where(Individuals.id == ind_id)
      data['indiv'] = dict(DBSession.execute(query).fetchone())
      # Last known location
      c = V_Individuals_LatLonDate.c
      query = select([c.lat, c.lon, c.date]).where(c.ind_id == ind_id).order_by(desc(c.date)).limit(1)
      lat, lon, date = DBSession.execute(query).fetchone()
      data['indiv']['last_loc'] = {'date':str(date), 'lat':float(lat), 'lon':float(lon)}

   return data