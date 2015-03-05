from array import array

from pyramid.view import view_config

from sqlalchemy import func, desc, select, union, union_all, and_, bindparam, update, or_, literal_column, join, text

from pyramid.httpexceptions import HTTPBadRequest
from ecorelevesensor.utils.data_toXML import data_to_XML
import pandas as pd
import numpy as np
import transaction, time
from ecorelevesensor.models import DBSession
from ecorelevesensor.models.sensor import Argos, Gps
from ecorelevesensor.models import Individual, dbConfig
from ecorelevesensor.models.data import (
	V_dataARGOS_withIndivEquip,
	V_dataGPS_withIndivEquip,
	ProtocolArgos,
	ProtocolGps,
	ProtocolIndividualEquipment,
	SatTrx,
	Station,
	V_Individuals_LatLonDate
)
from ecorelevesensor.utils.distance import haversine

route_prefix = 'argos/'

# List all PTTs having unchecked locations, with individual id and number of locations.
@view_config(
		route_name='{type}/unchecked/list',
    	# permission='read',
		renderer='json')
def argos_unchecked_list(request):
		"""Returns the unchecked Argos data summary.
		"""
		type_= request.matchdict['type']
		if type_ == 'argos' :
			unchecked = V_dataARGOS_withIndivEquip
		elif type_ == 'gps' :
			unchecked = V_dataGPS_withIndivEquip
		elif type_ == 'gsm' :
			unchecked = V_dataGSM_withIndivEquip

		print('________________________________________________________\n\n')

		unchecked_with_ind = select([unchecked.ptt.label('platform_'), unchecked.ind_id, unchecked.begin_date, unchecked.end_date, func.count().label('nb'), func.max(unchecked.date_).label('max_date'), func.min(unchecked.date_).label('min_date')]).where(unchecked.checked == 0).group_by(unchecked.ptt, unchecked.ind_id, unchecked.begin_date, unchecked.end_date).order_by(unchecked.ptt)
		# Populate Json array
		print(unchecked_with_ind)
		data = DBSession.execute(unchecked_with_ind).fetchall()
		print(data)
		return [dict(row) for row in data]
		# SQL query
		# unchecked = union_all(
		#     select([
		#         Argos.pk,
		#         Argos.ptt.label('ptt'),
		#         Argos.date
		#     ]).where(Argos.checked == False),
		#     select([
		#         Gps.pk,
		#         Gps.ptt.label('ptt'),
		#         Gps.date
		#     ]).where(Gps.checked == False)
		# ).alias()
		# # Add the bird associated to each ptt.
		# pie = ProtocolIndividualEquipment
		# unchecked_with_ind = select([
		#     pie.ind_id.label('ind_id'),
		#     'ptt',
		#     func.count().label('nb')
		# ]).select_from(
		#     unchecked.join(SatTrx, SatTrx.ptt == unchecked.c.ptt)
		#     .outerjoin(
		#         pie,
		#         and_(SatTrx.id == pie.sat_id,
		#              unchecked.c.date >= pie.begin_date,
		#              or_(
		#                  unchecked.c.date < pie.end_date,
		#                  pie.end_date == None
		#             )
		#         )
		#     )
		# ).group_by('ptt', pie.ind_id).order_by('ptt')
		# # Populate Json array
		# data = DBSession.execute(unchecked_with_ind).fetchall()
		# return [{'ptt':ptt,'ind_id':ind_id, 'count':nb} for ind_id, ptt, nb in data]

	

@view_config(route_name=route_prefix + 'unchecked/count', renderer='json')
def argos_unchecked_count(request):
		"""Returns the unchecked argos data count."""
		return DBSession.query(func.count(Argos.pk)
				).filter(Argos.checked == False).scalar()
	 
@view_config(route_name = 'gps/unchecked/count', renderer = 'json')
def gps_unchecked_count(request):
		"""Returns the unchecked gps data count."""
		return {'count': DBSession.query(func.count(Gps.pk)
				).filter(Gps.checked == 0).scalar()}

@view_config(route_name = 'argos/import', renderer = 'json')
def argos_manual_validate(request) :

	ptt = request.matchdict['id']
	data = request.json_body.get('data')
	ind_id = request.matchdict['ind_id']
	type_ = request.matchdict['type']
	dict_proc = {
	'argos':'[sp_validate_argos]',
	'gps' : '[sp_validate_gps]'
	}
	
	xml_to_insert = data_to_XML(data)
	'''validate unchecked ARGOS_ARGOS or ARGOS_GPS data from xml data PK_id.
	'''
	start = time.time()

	# push xml data to insert into stored procedure in order ==> create stations and protocols if not exist
	stmt = text(""" DECLARE @nb_insert int , @exist int, @error int;

		exec """+ dbConfig['data_schema'] + """."""+dict_proc[type_]+""":id_list, :ind_id , :user , :ptt , @nb_insert OUTPUT, @exist OUTPUT , @error OUTPUT;
	        SELECT @nb_insert, @exist, @error; """
	    ).bindparams(bindparam('id_list', xml_to_insert),bindparam('ind_id', ind_id),bindparam('user', user),bindparam('ptt', ptt))
	nb_insert, exist , error = DBSession.execute(stmt).fetchone()
	transaction.commit()

	stop = time.time()
	print ('\n time to insert '+str(stop-start))
	return str(nb_insert)+' stations/protocols was inserted, '+str(exist)+' are already existing and '+str(error)+' error(s)'

@view_config(route_name=route_prefix + 'import/auto', renderer='json', request_method='POST')
def data_argos_validation_auto(request):

	ptt = request.matchdict['id']
	ind_id = request.matchdict['ind_id']
	type_ = request.matchdict['type']

	nb_insert, exist , error = auto_validate_argos_gps(ptt,ind_id,request.authenticated_userid,type_)
	return str(nb_insert)+' stations/protocols was inserted, '+str(exist)+' are already existing and '+str(error)+' error(s)'

@view_config(route_name=route_prefix + 'importAll/auto', renderer='json', request_method='POST')
def data_argos_ALL_validation_auto(request):
	unchecked_list = argos_unchecked_list(request)
	type_ = request.matchdict['type']
	Total_nb_insert = 0
	Total_exist = 0
	Total_error = 0
	start = time.time()

	for row in unchecked_list : 
		ptt = row['platform_']
		ind_id = row['ind_id']
		print (ind_id)
		if ind_id != None : 
			nb_insert, exist, error = auto_validate_argos_gps(ptt,ind_id,request.authenticated_userid, type_)
			Total_exist += exist
			Total_nb_insert += nb_insert
			Total_error += error
	print (str(Total_nb_insert)+' stations/protocols was inserted, '+str(Total_exist)+' are already existing')

	stop = time.time()
	print ('\n time to insert '+str(stop-start))
	return str(Total_nb_insert)+' stations/protocols was inserted, '+str(Total_exist)+' are already existingand '+str(Total_error)+' error(s)'


def auto_validate_argos_gps (ptt,ind_id,user,type_) :
	start = time.time()
	dict_proc = {
	'argos':'[sp_auto_validate_argos]',
	'gps' : '[sp_auto_validate_gps]'
	}
	stmt = text(""" DECLARE @nb_insert int , @exist int , @error int;

		exec """+ dbConfig['data_schema'] + """."""+dict_proc[type_]+""":ptt , :ind_id , :user , @nb_insert OUTPUT, @exist OUTPUT, @error OUTPUT;
	        SELECT @nb_insert, @exist, @error; """
	    ).bindparams(bindparam('ptt', ptt), bindparam('ind_id', ind_id),bindparam('user', user))
	nb_insert, exist , error= DBSession.execute(stmt).fetchone()
	transaction.commit()

	stop = time.time()
	print ('\n time to insert '+str(stop-start))
	return nb_insert, exist , error

# _________------ OLD -----_________

# def argos_insert(request):
# 	 stations = []
# 	 argos_id = array('i')
# 	 gps_id = array('i')

# 	 # Query that check for duplicate stations
# 	 check_duplicate_station = select([func.count(Station.id)]).where(
# 			 and_(Station.name == bindparam('name'), Station.lat == bindparam('lat'),
# 						Station.lon == bindparam('lon'), Station.ele == bindparam('ele')))
	 
# 	 # For each objet in the request body
# 	 for ptt_obj in request.json_body:
# 			ptt = ptt_obj['ptt']
# 			ind_id = ptt_obj['ind_id']
				 
# 			# For each location associated with this object
# 			for location in ptt_obj['locations']:
# 				 # Argos
# 				 if location['type'] == 0:
# 						# Get all the informations about the sensor data
# 						argos_data = DBSession.query(Argos).filter_by(id=location['id']).one()
# 						name = 'ARGOS_' + str(argos_data.ptt) + '_' + argos_data.date.strftime('%Y%m%d%H%M%S')
# 						if DBSession.execute(check_duplicate_station, {'name':name, 'lat':argos_data.lat, 'lon':argos_data.lon, 'ele':argos_data.ele}).scalar() == 0:
# 							 argos = ProtocolArgos(ind_id=ind_id, lc=argos_data.lc, iq=argos_data.iq, nbMsg=argos_data.nbMsg, nbMsg120=argos_data.nbMsg120,
# 																			 bestLvl=argos_data.bestLvl, passDuration=argos_data.passDuration, nopc=argos_data.nopc, frequency=argos_data.frequency)
# 							 station = Station(date=argos_data.date, name=name, fieldActivityId=27, fieldActivityName='Argos', lat=argos_data.lat, lon=argos_data.lon, ele=argos_data.ele, protocol_argos=argos)
# 							 # Add the station in the list
# 							 argos_id.append(location['id'])
# 							 stations.append(station)
# 				 # Gps
# 				 elif location['type'] == 1:
# 						gps_data = DBSession.query(Gps).filter_by(id=location['id']).one()
# 						name = 'ARGOS_' + str(gps_data.ptt) + '_' + gps_data.date.strftime('%Y%m%d%H%M%S')
# 						if DBSession.execute(check_duplicate_station, {'name':name, 'lat':argos_data.lat, 'lon':argos_data.lon, 'ele':argos_data.ele}).scalar() == 0:    
# 							 gps = ProtocolGps(ind_id=ind_id, course=gps_data.course, speed=gps_data.speed)
# 							 station = Station(date=argos_data.date, name=name, fieldActivityId=27, fieldActivityName='Argos', lat=argos_data.lat, lon=argos_data.lon, ele=argos_data.ele, protocol_gps=gps)
# 							 # Add the station in the list
# 							 gps_id.append(location['id'])
# 							 stations.append(station)
# 	 # Insert the stations (and protocols thanks to ORM)
# 	 DBSession.add_all(stations)
# 	 # Update the sensor database
# 	 DBSession.execute(update(Argos).where(Argos.id.in_(argos_id)).values(checked=True, imported=True))
# 	 DBSession.execute(update(Gps).where(Gps.id.in_(gps_id)).values(checked=True, imported=True))
# 	 return {'status':'ok'}

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


@view_config(route_name= 'argos/details', renderer='json')
def indiv_details(request):
	type_= request.matchdict['type']
	if type_ == 'argos' :
		unchecked = V_dataARGOS_withIndivEquip
	elif type_ == 'gps' :
		unchecked = V_dataGPS_withIndivEquip

	print('_____DETAILS____')
	ptt = int(request.matchdict['id'])

	ind_id = int(request.matchdict['ind_id'])

	print(ind_id)
	print(ptt)
	join_table = join(Individual,unchecked, Individual.id == unchecked.ind_id) 

	query = select([Individual.id.label('ind_id'),
		Individual.survey_type.label('survey_type'),
		Individual.status.label('status'),
		Individual.monitoring_status.label('monitoring_status'),
		Individual.ptt.label('ptt'),
		Individual.species.label('species'),
		Individual.breeding_ring.label('breeding_ring'),
		Individual.release_ring.label('release_ring'),
		Individual.chip_code.label('chip_code'),
		Individual.sex.label('sex'),
		Individual.origin.label('origin'),
		Individual.age.label('age'),
		unchecked.begin_date,
		unchecked.end_date]).select_from(join_table).where(and_(unchecked.ptt == ptt,unchecked.ind_id == ind_id)
															  ).order_by(desc(unchecked.begin_date))
	print(query)
	data = DBSession.execute(query).first()
	transaction.commit()
	# if data['end_date'] == None :
	#     end_date=datetime.datetime.now()
	# else :
	#     end_date=data['end_date']

	result = dict([ (key[0],key[1]) for key in data.items()])
	print(result)
	# result['duration']=(end_date.month-data['begin_date'].month)+(end_date.year-data['begin_date'].year)*12
	
	query = select([V_Individuals_LatLonDate.c.date]).where(V_Individuals_LatLonDate.c.ind_id == result['ind_id']).order_by(desc(V_Individuals_LatLonDate.c.date)).limit(1)
	 
	lastObs = DBSession.execute(query).fetchone()
	result['last_observation'] = lastObs['date'].strftime('%d/%m/%Y')

	result['ptt'] = ptt
	print(result)
	return result

# Unchecked data for one PTT.
@view_config(route_name='argos/unchecked/geo', renderer='json')
def argos_unchecked_geo(request):
	"""Returns list of unchecked locations for a given ptt."""
	type_= request.matchdict['type']
	if type_ == 'argos' :
		unchecked = V_dataARGOS_withIndivEquip
	elif type_ == 'gps' :
		unchecked = V_dataGPS_withIndivEquip


	platform = int(request.matchdict['id'])

	if (request.matchdict['ind_id'] != 'null') :
		ind_id = int(request.matchdict['ind_id'])
	else :
		ind_id = None

	# unchecked = select([
	# 		DataGsm.platform_,
	# 		DataGsm.date.label('date'),
	# 		DataGsm.id.label('id'),
	# 		DataGsm.lat.label('lat'),
	# 		DataGsm.lon.label('lon'),
	# 		DataGsm.ele.label('ele'),
	# 	]).alias()

	query = select([unchecked.data_PK_ID.label('id'),
		unchecked.lat,
		unchecked.lon,
		unchecked.date_.label('date'),
		unchecked.ele]).where(and_(unchecked.ptt == platform,unchecked.ind_id == ind_id)).order_by(desc(unchecked.date_))

	data = DBSession.execute(query).fetchall()

	
		# Query
		# query = select([
		#     DataGsm.id.label('id'),
		#     DataGsm.lat,
		#     DataGsm.lon,
		#     DataGsm.date
		# ]).where(DataGsm.platform_ == platform).where(DataGsm.checked == False
		# ).order_by(desc(DataGsm.date)).limit(1000)
		# # Create list of features from query result

	features = [
		{
			'type':'Feature',
			'properties':{'date':str(date)},
			'geometry':{'type':'Point', 'coordinates':[float(lon),float(lat)]},
			'id':id_
		}
	for id_, lat, lon, date, ele in data]
	transaction.commit()
	result = {'type':'FeatureCollection', 'features':features}
	return result

@view_config(route_name='argos/unchecked/json', renderer='json')
def argos_unchecked_json(request):	
		type_= request.matchdict['type']
		if type_ == 'argos' :
			unchecked = V_dataARGOS_withIndivEquip
		elif type_ == 'gps' :
			unchecked = V_dataGPS_withIndivEquip


		platform = int(request.matchdict['id'])

		if (request.matchdict['ind_id'] != 'null') :
			ind_id = int(request.matchdict['ind_id'])
		else :
			ind_id = None

	# unchecked = select([
	# 		DataGsm.platform_,
	# 		DataGsm.date.label('date'),
	# 		DataGsm.id.label('id'),
	# 		DataGsm.lat.label('lat'),
	# 		DataGsm.lon.label('lon'),
	# 		DataGsm.ele.label('ele'),
	# 	]).alias()
		query = select([unchecked.data_PK_ID.label('id'),
		unchecked.lat,
		unchecked.lon,
		unchecked.date_.label('date'),
		unchecked.ele]).where(and_(unchecked.ptt == platform,unchecked.ind_id == ind_id)).order_by(desc(unchecked.date_))

		data = DBSession.execute(query).fetchall()	
		# Query
		# query = select([
		#     DataGsm.id.label('id'),
		#     DataGsm.lat.label('lat'),
		#     DataGsm.lon.label('lon'),
		#     DataGsm.ele.label('ele'),
		#     DataGsm.date.label('date')]
		# ).where(DataGsm.platform_ == platform
		# ).where(DataGsm.checked == False
		# ).order_by(desc(DataGsm.date))
		# data = DBSession.execute(query).fetchall()

		# Load data from the DB then
		# compute the distance between 2 consecutive points.
		 
		df = pd.DataFrame.from_records(data, columns=data[0].keys(), coerce_float=True)
		X1 = df.iloc[:-1][['lat', 'lon']].values
		X2 = df.iloc[1:][['lat', 'lon']].values
		df['dist'] = np.append(haversine(X1, X2), 0).round(3)
		# Compute the speed
		df['speed'] = (df['dist'] / ((df['date'] - df['date'].shift(-1)).fillna(1) / np.timedelta64(1, 'h'))).round(3)
		# Values to import : the first per hour
		ids = df.set_index('date').resample('1H', how='first').dropna().id.values
		df['import'] = df.id.isin(ids)
		df['date'] = df['date'].apply(str) 
		# Fill NaN
		df.fillna(value={'ele':-999}, inplace=True)
		df.fillna(value={'speed':0}, inplace=True)
		return df.to_dict('records')
		# ptt is a mandatory parameter.




		# try:
		# 		ptt = int(request.GET['ptt'])
		# except:
		# 		raise HTTPBadRequest()

		# # Get all unchecked data for this ptt and this individual
		# # Type 0 = Argos data, type 1 = GPS data
		# argos_data = select([
		# 		Argos.pk.label('pk'), 
		# 		Argos.date,
		# 		Argos.lat,
		# 		Argos.lon,
		# 		Argos.lc,
		# 		literal_column('0').label('type')
		# ]).where(Argos.checked == False).where(Argos.ptt == ptt)
		# gps_data = select([
		# 		Gps.pk.label('pk'),
		# 		Gps.date,
		# 		Gps.lat,
		# 		Gps.lon,
		# 		literal_column('NULL').label('lc'),
		# 		literal_column('1').label('type')
		# ]).where(Gps.checked == False).where(Gps.ptt == ptt)
		# unchecked = union(argos_data, gps_data).alias('unchecked')
		
		# # ind_id is a facultative parameter
		# try:
		# 		ind_id = int(request.GET['ind_id'])
		# 		all_data = select([
		# 				unchecked.c.pk,
		# 				unchecked.c.date,
		# 				unchecked.c.lat,
		# 				unchecked.c.lon,
		# 				unchecked.c.lc,
		# 				unchecked.c.type
		# 		]).select_from(unchecked
		# 				.join(SatTrx, SatTrx.ptt == ptt)
		# 				.join(ProtocolIndividualEquipment,
		# 						and_(
		# 								SatTrx.id == ProtocolIndividualEquipment.sat_id,
		# 								unchecked.c.date >= ProtocolIndividualEquipment.begin_date,
		# 								or_(
		# 										unchecked.c.date < ProtocolIndividualEquipment.end_date,
		# 										ProtocolIndividualEquipment.end_date == None
		# 								)
		# 						)
		# 				)
		# 		).where(ProtocolIndividualEquipment.ind_id == ind_id)
		# except KeyError or TypeError:
		# 		all_data = select([
		# 				unchecked.c.pk,
		# 				unchecked.c.date,
		# 				unchecked.c.lat,
		# 				unchecked.c.lon,
		# 				unchecked.c.lc,
		# 				unchecked.c.type
		# 		])
		# 		ind_id = None

		# # Initialize json object
		# result = {'ptt':{}, 'locations':[], 'indiv':{}}
	 
		# # Load data from the DB then
		# # compute the distance between 2 consecutive points.
		# data = DBSession.execute(all_data.order_by(desc(all_data.c.date))).fetchall()
		# df = pd.DataFrame.from_records(data, columns=data[0].keys(), coerce_float=True)
		# X1 = df.ix[:,['lat', 'lon']].values[:-1,:]
		# X2 = df.ix[1:,['lat', 'lon']].values
		# dist = pd.Series(np.append(haversine(X1, X2).round(3), 0), name='dist')
		# df = pd.concat([df['pk'], df['date'].apply(lambda x: str(x)), df['lat'], df['lon'], df['lc'], df['type'], dist], axis=1)
		# result['locations'] = df.to_dict('records')

		# # Get informations for this ptt
		# ptt_infos = select([SatTrx.ptt, SatTrx.manufacturer, SatTrx.model]).where(SatTrx.ptt == ptt)
		# result['ptt']['ptt'], result['ptt']['manufacturer'], result['ptt']['model'] = DBSession.execute(ptt_infos).fetchone()

		# # Get informations for the individual
		# if ind_id is not None:
		# 		query = select([
		# 				Individual.id.label('id'),
		# 				Individual.age.label('age'),
		# 				Individual.sex.label('sex'),
		# 				Individual.specie.label('specie'),
		# 				Individual.monitoring_status.label('monitoring_status'), 
		# 				Individual.origin.label('origin'),
		# 				Individual.survey_type.label('survey_type')
		# 		]).where(Individual.id == ind_id)
		# 		result['indiv'] = dict(DBSession.execute(query).fetchone())
		# 		# Last known location
		# 		c = V_Individuals_LatLonDate.c
		# 		query = select([c.lat, c.lon, c.date]).where(c.ind_id == ind_id).order_by(desc(c.date)).limit(1)
		# 		lat, lon, date = DBSession.execute(query).fetchone()
		# 		result['indiv']['last_loc'] = {'date':str(date), 'lat':float(lat), 'lon':float(lon)}
		# return result
