from array import array

from pyramid.view import view_config
from pyramid.response import Response
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
	V_dataARGOS_GPS_with_IndivEquip,
	ProtocolArgos,
	ProtocolGps,
	ProtocolIndividualEquipment,
	SatTrx,
	Station,
	V_Individuals_LatLonDate
)
from ecorelevesensor.utils.distance import haversine

route_prefix = 'argos/'
def asInt(s):
	try:
		return int(s)
	except:
		return None
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
			unchecked = V_dataARGOS_GPS_with_IndivEquip
		elif type_ == 'gsm' :
			unchecked = V_dataGSM_withIndivEquip

		print('________________________________________________________\n\n')

		unchecked_with_ind = select([unchecked.ptt.label('platform_'), unchecked.ind_id, unchecked.begin_date, unchecked.end_date, func.count().label('nb'), func.max(unchecked.date_).label('max_date'), func.min(unchecked.date_).label('min_date')]).where(unchecked.checked == 0).group_by(unchecked.ptt, unchecked.ind_id, unchecked.begin_date, unchecked.end_date).order_by(unchecked.ptt)
		# Populate Json array
		print(unchecked_with_ind)
		data = DBSession.execute(unchecked_with_ind).fetchall()
		print(data)
		return [dict(row) for row in data]


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
	ind_id = asInt(ind_id)
	
	try : 
		if isinstance( ind_id, int ): 
			xml_to_insert = data_to_XML(data)
			'''validate unchecked ARGOS_ARGOS or ARGOS_GPS data from xml data PK_id.
			'''
			start = time.time()

			# push xml data to insert into stored procedure in order ==> create stations and protocols if not exist
			stmt = text(""" DECLARE @nb_insert int , @exist int, @error int;

				exec """+ dbConfig['data_schema'] + """.[sp_validate_argosArgos_argosGPS] :id_list, :ind_id , :user , :ptt , @nb_insert OUTPUT, @exist OUTPUT , @error OUTPUT;
			        SELECT @nb_insert, @exist, @error; """
			    ).bindparams(bindparam('id_list', xml_to_insert),bindparam('ind_id', ind_id),bindparam('user', request.authenticated_userid),bindparam('ptt', ptt))
			nb_insert, exist , error = DBSession.execute(stmt).fetchone()
			transaction.commit()

			stop = time.time()
			print ('\n time to insert '+str(stop-start))
			return str(nb_insert)+' stations/protocols was inserted, '+str(exist)+' are already existing and '+str(error)+' error(s)'
		else : 
			return error_response(None)
	except  Exception as err :
		return error_response(err)

@view_config(route_name=route_prefix + 'import/auto', renderer='json', request_method='POST')
def data_argos_validation_auto(request):
	try :
		ptt = request.matchdict['id']
		ind_id = request.matchdict['ind_id']
		type_ = request.matchdict['type']
		ind_id = asInt(ind_id)

		
		if isinstance( ind_id, int ): 
			nb_insert, exist , error = auto_validate_argos_gps(ptt,ind_id,request.authenticated_userid,type_)
			return str(nb_insert)+' stations/protocols was inserted, '+str(exist)+' are already existing and '+str(error)+' error(s)'
		else : 
			return error_response(None)
	except  Exception as err :
		return error_response(err)

def error_response (err) : 
		
		if err !=None : 
			msg = err.args[0] if err.args else ""
			response=Response('Problem occurs : '+str(type(err))+' = '+msg)
		else : 
			response=Response('No induvidual is equiped with this ptt at this date')
		response.status_int = 500
		return response

@view_config(route_name=route_prefix + 'importAll/auto', renderer='json', request_method='POST')
def data_argos_ALL_validation_auto(request):
	unchecked_list = argos_unchecked_list(request)
	type_ = request.matchdict['type']
	Total_nb_insert = 0
	Total_exist = 0
	Total_error = 0
	start = time.time()
	try : 
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
	except  Exception as err :

		msg = err.args[0] if err.args else ""
		response=Response('Problem occurs  : '+str(type(err))+' = '+msg)
		response.status_int = 500
		return response

def auto_validate_argos_gps (ptt,ind_id,user,type_) :
	start = time.time()
	stmt = text(""" DECLARE @nb_insert int , @exist int , @error int;

		exec """+ dbConfig['data_schema'] + """.[sp_auto_validate_argosArgos_argosGPS] :ptt , :ind_id , :user , @nb_insert OUTPUT, @exist OUTPUT, @error OUTPUT;
	        SELECT @nb_insert, @exist, @error; """
	    ).bindparams(bindparam('ptt', ptt), bindparam('ind_id', ind_id),bindparam('user', user))
	nb_insert, exist , error= DBSession.execute(stmt).fetchone()
	transaction.commit()

	stop = time.time()
	print ('\n time to insert '+str(stop-start))
	return nb_insert, exist , error

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

	unchecked = V_dataARGOS_GPS_with_IndivEquip


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
	unchecked = V_dataARGOS_GPS_with_IndivEquip
	platform = int(request.matchdict['id'])

	if (request.matchdict['ind_id'] != 'null') :
		ind_id = int(request.matchdict['ind_id'])
	else :
		ind_id = None

	query = select([unchecked.data_PK_ID.label('id'),
		unchecked.lat,
		unchecked.lon,
		unchecked.date_.label('date'),
		unchecked.ele,
		unchecked.type_]).where(and_(unchecked.ptt == platform,unchecked.ind_id == ind_id)).order_by(desc(unchecked.date_))

	data = DBSession.execute(query).fetchall()

	features = [
		{
			'type':'Feature',
			'properties':{'id':id_,'date':str(date),'type':type_},
			'geometry':{'type':'Point', 'coordinates':[float(lon),float(lat)]},
			
		}
	for id_, lat, lon, date, ele, type_ in data]
	transaction.commit()
	result = {'type':'FeatureCollection', 'features':features}
	return result

@view_config(route_name='argos/unchecked/json', renderer='json')
def argos_unchecked_json(request):	
		type_= request.matchdict['type']

		unchecked = V_dataARGOS_GPS_with_IndivEquip



		platform = int(request.matchdict['id'])

		if (request.matchdict['ind_id'] != 'null') :
			ind_id = int(request.matchdict['ind_id'])
		else :
			ind_id = None
		query = select([unchecked.data_PK_ID.label('id'),
		unchecked.lat,
		unchecked.lon,
		unchecked.date_.label('date'),
		unchecked.ele,
		unchecked.type_]).where(and_(unchecked.ptt == platform,unchecked.ind_id == ind_id)).order_by(desc(unchecked.date_))

		data = DBSession.execute(query).fetchall()	
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

