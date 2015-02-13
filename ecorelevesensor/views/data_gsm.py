"""
Created on Tue Sep 23 17:15:47 2014
@author: Natural Solutions (Thomas)
"""

from pyramid.view import view_config
from sqlalchemy import desc, select, func,text, insert, join, Integer, cast, and_, Float, or_,bindparam, update, outerjoin
from ecorelevesensor.models import (AnimalLocation,V_ProtocolIndividualEquipment,V_EquipGSM,
	DBSession, DataGsm, SatTrx, V_dataGSM_withIndivEquip, Station,
	ObjectsCaracValues, Individual,V_Individuals_LatLonDate,dbConfig )

from ecorelevesensor.utils.generator import Generator

from ecorelevesensor.utils.distance import haversine
from traceback import print_exc
import pandas as pd
import numpy as np
import re
import datetime,transaction,json

gene= Generator('T_DataGsm')

prefix = 'dataGsm/'

@view_config(route_name=prefix + 'unchecked/list', renderer='json')
def data_gsm_unchecked_list(request):
	'''List unchecked GSM data.
	'''
	unchecked = select([
		DataGsm.platform_,
		DataGsm.date
	]).alias()


	unchecked = V_dataGSM_withIndivEquip

	print ('________________________________________________________\n\n')

	unchecked_with_ind = select([
		unchecked.ptt.label('platform_'), unchecked.ind_id, unchecked.begin_date, unchecked.end_date, func.count().label('nb')
	]).group_by(unchecked.ptt, unchecked.ind_id, unchecked.begin_date, unchecked.end_date).order_by(unchecked.ptt)
	# Populate Json array
	print (unchecked_with_ind)
	data = DBSession.execute(unchecked_with_ind).fetchall()
	print (data)
	return [dict(row) for row in data]

@view_config(route_name=prefix + 'unchecked', renderer='json')
def data_gsm_unchecked(request):
	'''Get the unchecked GSM data.
	'''
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

	unchecked = V_dataGSM_withIndivEquip
	query = select([
		unchecked.data_PK_ID.label('id'),
		unchecked.lat,
		unchecked.lon,
		unchecked.date_.label('date'),
		unchecked.ele
		]).where(and_(unchecked.ptt == platform,unchecked.ind_id == ind_id)).order_by(desc(unchecked.date_))

	data = DBSession.execute(query).fetchall()

	if request.GET['format'] == 'geojson':
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
		
	elif request.GET['format'] == 'json':
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
		df['speed'] = (df['dist']/((df['date']-df['date'].shift(-1)).fillna(1)/np.timedelta64(1, 'h'))).round(3)
		# Values to import : the first per hour
		ids = df.set_index('date').resample('1H', how='first').dropna().id.values
		df['import'] = df.id.isin(ids)
		df['date'] = df['date'].apply(str) 
		# Fill NaN
		df.fillna(value={'ele':-999}, inplace=True)
		return df.to_dict('records')
		
@view_config(route_name=prefix + 'unchecked/import', renderer='json', request_method='POST')
def data_gsm_unchecked_import(request):
	'''Import unchecked GSM data.
	'''
	print('____--- Import Check ---___')
	ptt=request.matchdict['id']
	data = request.json_body.get('data')
	id_ind=request.json_body.get('id_ind')
	print(ptt)
	print(id_ind)
	
	# it = iter(data)
	check_duplicate_station = select([func.count(Station.id)]).where(
		and_(Station.name == bindparam('name'), Station.lat == bindparam('lat'),
			Station.lon == bindparam('lon'), Station.ele == bindparam('ele')))
	# if (len(data)> 2100) :

	# gsm_data = DBSession.execute(select([DataGsm.lat,DataGsm.lon,DataGsm.date, DataGsm.ele, DataGsm.platform_]).where(DataGsm.id.in_(data))).fetchall()
	

	# id_data_to_insert = []
	

	# all_gsm_data = []
	# i = 0
	# if (len(data)> 2100) :
	# 	while i < len(data)-1 :
	# 		j = i
	# 		i += 2000
	# 		if i > len(data)-1 :
	# 			i=len(data)-1
	# 		part_gsm_data = DBSession.query(DataGsm).filter(DataGsm.id.in_(data[j:i])).all()
	# 		all_gsm_data.append(list(part_gsm_data))
	# print (len(data))
	# print('____________________all_gsm_data__________________\n')
	# print (len(all_gsm_data))
	# print(all_gsm_data)


	# for id_ in data :
	# 	name = 'ARGOS_' + str(gsm_data.platform_) + '_' + gsm_data.date.strftime('%Y%m%d%H%M%S')

	# 	if DBSession.execute(check_duplicate_station, {'name':name, 'lat':gsm_data.lat, 'lon':gsm_data.lon, 'ele':gsm_data.ele}).scalar() == 0:
	# 		id_data_to_insert.append(gsm_data.id)
	# print (len(id_data_to_insert))
	

	#query = update(DataGsm).where(DataGsm.data_PK_ID.in_(data)).values(validated = 1)

	# DBSession.execute(query)
	# # select_stmt = DBSession.execute(select([DataGsm.lat,DataGsm.lon,DataGsm.date],DataGsm.id.in_(data))).fetchall()
	# # print (select_stmt)
	# # query = insert(AnimalLocation, select_stmt)
	# # DBSession.execute(query)
	# stmt = text("""
	# 	DECLARE @nb int;
	# 	EXEC """ + dbConfig['data_schema'] + """.sp_validate_gsm :ind, :user , :platform , @nb OUTPUT;
	# 	SELECT @nb;"""
	# ).bindparams(bindparam('user', request.authenticated_userid),bindparam('platform', ptt),bindparam('ind', id_ind))
	

	# nb = DBSession.execute(stmt).fetchone()
	# print(nb)



	# if error_code == 0:
	# 	if nb > 0:
	# 		return 'Success : ' + str(nb) + ' new rows inserted in table T_AnimalLocation.'
	# 	else:
	# 		return 'Warning : no new row inserted.'
	# else:
	# 	return 'Error : an error occured during validation process (error code : ' + str(error_code) + ' )'


	
def asInt(s):
	try:
		return int(s)
	except:
		return None
	
@view_config(route_name=prefix + 'upload', renderer='string')
def data_gsm_all(request):
	'''Import unchecked GSM data.
	'''
	response = 'Success'
	ptt_pattern = re.compile('[0]*(?P<platform>[0-9]+)g')
	try:
		file = request.POST['file'].file
		filename = request.POST['file'].filename
		print(ptt_pattern.search(filename))
		platform = int(ptt_pattern.search(filename).group('platform'))
		query = select([DataGsm.date]).where(DataGsm.platform_ == platform)
		# Read dates that are already in the database
		df = pd.DataFrame.from_records(DBSession.execute(query).fetchall(), index=DataGsm.date.name, columns=[DataGsm.date.name])
		# Load raw csv data
		csv_data = pd.read_csv(file, sep='\t',
			index_col=0,
			parse_dates=True,
			# Read those values as NaN
			na_values=['No Fix', 'Batt Drain', 'Low Voltage'],
			# Only import the first 8 columns
			usecols=range(9)
		)
		# Remove the lines containing NaN
		csv_data.dropna(inplace=True)
		# Filter data with no elevation by converting the column to numeric type
		csv_data[DataGsm.ele.name] = csv_data[DataGsm.ele.name].convert_objects(convert_numeric=True)
		# Get the data to insert
		data_to_insert = csv_data[~csv_data.index.isin(df.index)]
		# Add the platform to the DataFrame
		data_to_insert[DataGsm.platform_.name] = platform
		# Write into the database
		data_to_insert.to_sql(DataGsm.__table__.name, DBSession.get_bind(), if_exists='append')
	except:
		print_exc()
		response = 'An error occured.'
		request.response.status_code = 500
	return response

@view_config(route_name=prefix + 'details', renderer='json')
def indiv_details(request):
	print('_____DETAILS____')
	ptt=int(request.matchdict['id'])

	ind_id=int(request.matchdict['ind_id'])

	print(ind_id)
	print(ptt)
	join_table = join(SatTrx, ObjectsCaracValues, SatTrx.ptt == cast(ObjectsCaracValues.value, Integer)
		).join(Individual, ObjectsCaracValues.object==Individual.id) 

	query=select([
		Individual.id.label('ind_id'),
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
		Individual.age.label('age')]
		).select_from(join_table
		).where(and_(SatTrx.model.like('GSM%'),ObjectsCaracValues.carac_type==19,ObjectsCaracValues.object_type=='Individual')
		).where(ObjectsCaracValues.value==ptt).order_by(desc(ObjectsCaracValues.begin_date))
	print (query)
	data=DBSession.execute(query).first()
	transaction.commit()
	# if data['end_date'] == None :
	#     end_date=datetime.datetime.now()
	# else :
	#     end_date=data['end_date'] 

	result=dict([ (key[0],key[1]) for key in data.items()])
	print(result)
	# result['duration']=(end_date.month-data['begin_date'].month)+(end_date.year-data['begin_date'].year)*12
	
	query = select([V_Individuals_LatLonDate.c.date]
					 ).where(V_Individuals_LatLonDate.c.ind_id == result['ind_id']
					 ).order_by(desc(V_Individuals_LatLonDate.c.date)).limit(1)
	 
	lastObs=DBSession.execute(query).fetchone()
	result['last_observation']=lastObs['date'].strftime('%d/%m/%Y')

	result['ptt'] = ptt
	print (result)
	return result

	# q_indiv=select([
	# 	Individual.id.label('ind_id'),
	# 	Individual.survey_type.label('survey_type'),
	# 	Individual.status.label('status'),
	# 	Individual.monitoring_status.label('monitoring_status'),
	# 	Individual.ptt.label('ptt'),
	# 	Individual.species.label('species'),
	# 	Individual.breeding_ring.label('breeding_ring'),
	# 	Individual.release_ring.label('release_ring'),
	# 	Individual.chip_code.label('chip_code'),
	# 	Individual.sex.label('sex'),
	# 	Individual.origin.label('origin'),
	# 	Individual.age.label('age')
	# ]).where(Individual.id==ind_id)

	# data=DBSession.execute(q_indiv).fetchone()
	# result=dict([ (key[0],key[1]) for key in data.items()])


	# ##### Retrieve Number of location and duration  #####
	# unchecked = select([
	# 	DataGsm.platform_,
	# 	DataGsm.date
	# ]).alias()

	# pie = V_ProtocolIndividualEquipment
	# unchecked_with_ind = select([
	# 	pie.begin_date.label('begin_date'),
	# 	pie.end_date.label('end_date'),
	# 	func.count().label('nb')
	# ]).select_from(
	# 	unchecked.join(SatTrx, SatTrx.ptt == unchecked.c.platform_)
	# 	.outerjoin(
	# 		pie,
	# 		and_(SatTrx.id == pie.sat_id,
	# 			 unchecked.c['DateTime'] >= pie.begin_date,
	# 			 or_(
	# 				 unchecked.c['DateTime'] < pie.end_date,
	# 				 pie.end_date == None
	# 			)
	# 		)
	# 	)
	# ).where(and_(pie.ind_id==ind_id,unchecked.c.platform_== ptt)
	# ).group_by(unchecked.c.platform_, pie.ind_id, pie.begin_date,pie.end_date)
	
	# nb = DBSession.execute(unchecked_with_ind).fetchone()
	# print('\n ________________________ \n \n')
	# print(nb)
	# # if nb['end_date'] == None :
	# # 	end_date=datetime.datetime.now()
	# # else :
	# # 	end_date=nb['end_date'] 
	# # result['duration'] = (end_date.month-nb['begin_date'].month)+(end_date.year-nb['begin_date'].year)*12
	# result['begin_date']= nb['begin_date']
	# result['end_date']= nb['end_date']
	# result['indivNbObs'] = nb['nb']
	# result['ptt'] = ptt

	# ##### Retrieve Last Observation recorded #####
	# q_lastObs = select([V_Individuals_LatLonDate.c.date]
	# 				 ).where(V_Individuals_LatLonDate.c.ind_id == ind_id
	# 				 ).order_by(desc(V_Individuals_LatLonDate.c.date)).limit(1)
	# lastObs = DBSession.execute(q_lastObs).fetchone()

	# result['last_observation'] = lastObs['date'].strftime('%d/%m/%Y')
	# # if result['birth_date'] != None:
	# # 	result['birth_date'] = result['birth_date'].strftime('%d/%m/%Y')

	# print (result)
	# return result
 