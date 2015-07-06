"""
Created on Tue Sep 23 17:15:47 2014
@author: Natural Solutions (Thomas)
"""
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import desc, select, func,text, insert, join, Integer, cast, and_, Float, or_,bindparam, update, outerjoin
from ecorelevesensor.models import (AnimalLocation,V_ProtocolIndividualEquipment,
    DBSession, DataGsm, EngineeringData , SatTrx, V_dataGSM_withIndivEquip, Station,V_dataARGOS_withIndivEquip,
    ObjectsCaracValues, Individual,V_Individuals_LatLonDate,dbConfig )
from ecorelevesensor.models.data import (
   ProtocolArgos,
   ProtocolGps)
from ecorelevesensor.models.sensor import Gsm, GsmEngineering
from ecorelevesensor.utils.generator import Generator

from ecorelevesensor.utils.distance import haversine
from ecorelevesensor.utils.data_toXML import data_to_XML

from traceback import print_exc
import pandas as pd
import numpy as np
import re
import datetime, time
import transaction
import json
from sqlalchemy.orm import query

gene = Generator('T_DataGsm')

prefix = 'dataGsm/'

@view_config(route_name=prefix + 'unchecked/list', renderer='json')
def data_gsm_unchecked_list(request):
    # List unchecked GSM data.  
    unchecked = select([DataGsm.platform_,
        DataGsm.date]).alias()
    unchecked = V_dataGSM_withIndivEquip
    unchecked_with_ind = select([unchecked.ptt.label('platform_'), unchecked.ind_id, unchecked.begin_date, unchecked.end_date, func.count().label('nb'), func.max(unchecked.date_).label('max_date'), func.min(unchecked.date_).label('min_date')]).where(unchecked.checked == 0).group_by(unchecked.ptt, unchecked.ind_id, unchecked.begin_date, unchecked.end_date).order_by(unchecked.ptt)
    data = DBSession.execute(unchecked_with_ind).fetchall()
    return [dict(row) for row in data]

@view_config(route_name=prefix + 'unchecked', renderer='json')
def data_gsm_unchecked(request):
    #Get the unchecked GSM data.
    platform = int(request.matchdict['id'])
    if (request.matchdict['ind_id'] != 'null') :
        ind_id = int(request.matchdict['ind_id'])
    else :
        ind_id = None

    unchecked = V_dataGSM_withIndivEquip
    query = select([unchecked.data_PK_ID.label('id'),
        unchecked.lat,
        unchecked.lon,
        unchecked.date_.label('date'),
        unchecked.ele]).where(and_(unchecked.checked == 0,and_(unchecked.ptt == platform,unchecked.ind_id == ind_id))).order_by(desc(unchecked.date_))
    data = DBSession.execute(query).fetchall()

    if request.GET['format'] == 'geojson':

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
        df.replace(to_replace = {'speed': np.inf}, value = {'speed':9999}, inplace = True)
        return df.to_dict('records')
        
@view_config(route_name=prefix + 'unchecked/import', renderer='json', request_method='POST')
def data_gsm_unchecked_import(request):

    ptt = request.matchdict['id']
    data = request.json_body.get('data')
    ind_id = request.matchdict['ind_id']
    xml_to_insert = data_to_XML(data)
    try : 
        ind_id = asInt(ind_id)
        if isinstance( ind_id, int ): 
            nb_insert, exist, error = gsm_unchecked_validation(ptt,ind_id,request.authenticated_userid,xml_to_insert)
            return str(nb_insert)+' stations/protocols was inserted, '+str(exist)+' are already existing'
        else : 
            return error_response(None)
    except  Exception as err :
        msg = err.args[0] if err.args else ""
        response=Response('Problem occurs on station update : '+str(type(err))+' = '+msg)
        response.status_int = 500
        return response

def gsm_unchecked_validation(ptt,ind_id,user,xml_to_insert):
    #validate unchecked GSM data from xml GSM data PK_id.   
    start = time.time()
    # push xml data to insert into stored procedure in order ==> create stations and protocols if not exist
    stmt = text(""" DECLARE @nb_insert int , @exist int, @error int;
        exec """+ dbConfig['data_schema'] + """.[sp_validate_gsm] :id_list, :ind_id , :user , :ptt , @nb_insert OUTPUT, @exist OUTPUT , @error OUTPUT;
            SELECT @nb_insert, @exist, @error; """
        ).bindparams(bindparam('id_list', xml_to_insert),bindparam('ind_id', ind_id),bindparam('user', user),bindparam('ptt', ptt))
    nb_insert, exist , error = DBSession.execute(stmt).fetchone()
    transaction.commit()
    stop = time.time()
    return nb_insert, exist, error
    
@view_config(route_name=prefix + 'unchecked/import/auto', renderer='json', request_method='POST')
def data_gsm_unchecked_validation_auto(request):

    ptt = request.matchdict['id']
    ind_id = request.matchdict['ind_id']
    param = request.json_body
    freq = param['frequency']
    try : 
        ind_id = asInt(ind_id)
        if isinstance( ind_id, int ): 
            nb_insert, exist , error = auto_validate_gsm(ptt,ind_id,request.authenticated_userid,freq)
            transaction.commit()
            return str(nb_insert)+' stations/protocols inserted, '+str(exist)+' existing and '+str(error)+' error(s)'
        else : 
            return error_response(None)
    except  Exception as err :
        return error_response(err)

@view_config(route_name=prefix + 'unchecked/importAll/auto', renderer='json', request_method='POST')
def data_gsm_uncheckedALL_validation_auto(request):
    unchecked_list = data_gsm_unchecked_list(request)
    Total_nb_insert = 0
    Total_exist = 0
    Total_error = 0
    start = time.time()
    param = request.json_body
    freq = param['frequency']
    try : 

        for row in unchecked_list : 
            ptt = row['platform_']
            ind_id = row['ind_id']
            if ind_id != None : 
                nb_insert, exist, error = auto_validate_gsm(ptt,ind_id,request.authenticated_userid,freq)
                Total_exist += exist
                Total_nb_insert += nb_insert
                Total_error += error
        transaction.commit()
        stop = time.time()
        return str(Total_nb_insert)+' stations/protocols inserted, '+str(Total_exist)+' existing and '+str(Total_error)+' error(s)'
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

def auto_validate_gsm (ptt,ind_id,user) :

    stmt = text(""" DECLARE @nb_insert int , @exist int , @error int;
        exec """+ dbConfig['data_schema'] + """.[sp_auto_validate_gsm] :ptt , :ind_id , :user ,:freq, @nb_insert OUTPUT, @exist OUTPUT, @error OUTPUT;
            SELECT @nb_insert, @exist, @error; """
        ).bindparams(bindparam('ptt', ptt), bindparam('ind_id', ind_id),bindparam('user', user),bindparam('freq', freq))
    nb_insert, exist , error= DBSession.execute(stmt).fetchone()
    transaction.commit()
    return nb_insert, exist , error
    
def asInt(s):
    try:
        return int(s)
    except:
        return None
    
@view_config(route_name=prefix + 'upload', renderer='string')
def data_gsm_all(request):
    #Import unchecked GSM data.
    response = 'Success'
    ptt_pattern = re.compile('[0]*(?P<platform>[0-9]+)g')
    eng_pattern = re.compile('[0]*(?P<platform>[0-9]+)e')
    ALL_ptt_pattern = re.compile('GPS')
    ALL_eng_pattern = re.compile('Engineering')

    dict_pattern = {
        'all_gps': ALL_ptt_pattern,
        'all_eng' : ALL_eng_pattern,
        'ptt_gps' : ptt_pattern,
        'ptt_eng' :eng_pattern
        }

    dict_func_data = {
        'all_gps': get_ALL_gps_toInsert,
        'all_eng' : get_ALL_eng_toInsert,
        'ptt_gps' : get_gps_toInsert,
        'ptt_eng' : get_eng_toInsert
        }
    res = None
    try:
        file_obj = request.POST['file']
        filename = request.POST['file'].filename
        for k in dict_pattern :
            if (dict_pattern[k].search(filename)) :
                res = dict_func_data[k](file_obj)
    except:
        print_exc()
        response = 'An error occured.'
        request.response.status_code = 500
    return (response,res)       

def get_ALL_gps_toInsert(file_obj) :
        file = file_obj.file
        # Load raw csv data
        csv_data = pd.read_csv(file, sep='\t',
            index_col=0,
            parse_dates=True,
            )
        # Remove the lines containing NaN and columns 
        csv_data.dropna(inplace=True)
        csv_data.drop(['SatelliteCount','ShowInKML','file_date'], axis=1, inplace=True)
        # get list of ptt
        platform_df = csv_data[['GSM_ID']]
        platform_df = platform_df.groupby('GSM_ID')['GSM_ID'].agg(['count'])
        platform_list = platform_df.index.get_values().tolist()             
        #go to insert data in the database
        return insert_GPS(platform_list, csv_data)
        
def get_gps_toInsert(file_obj) :
    file = file_obj.file
    filename=file_obj.filename
    ptt_pattern = re.compile('[0]*(?P<platform>[0-9]+)g')
    platform = int(ptt_pattern.search(filename).group('platform'))

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
    print(csv_data.columns)

    #go to insert data in the database
    return insert_GPS(platform, csv_data)

def insert_GPS(platform, csv_data) :

    if (type(platform) is list) :
        query = select([Gsm.date]).where(Gsm.platform_.in_(platform))
    elif (type(platform) is int) :
        query = select([Gsm.date]).where(Gsm.platform_ == platform) 
    else : return 'error type : "platform" '
    ## Read dates that are already in the database
    df = pd.DataFrame.from_records(DBSession.execute(query).fetchall(), index=Gsm.date.name, columns=[Gsm.date.name])
    ### Filter data with no elevation by converting the column to numeric type
    csv_data[Gsm.ele.name] = csv_data[Gsm.ele.name].convert_objects(convert_numeric=True)

    ### Get the data to insert
    data_to_insert = csv_data[~csv_data.index.isin(df.index)]
    #### Add the platform to the DataFrame
    if (type(platform) is int) :
        data_to_insert[Gsm.platform_.name] = platform
        res = {'new GPS data inserted' : data_to_insert.shape[0]}
    else : 
        if (data_to_insert.shape[0] != 0) :
            ptt_name = 'GSM_ID'
            platform_count = data_to_insert.groupby(ptt_name)[ptt_name].agg(['count'])
            res = platform_count.to_dict()
        else : 
            res = {'new GPS data inserted' : 0}
    ### Add the platform to the DataFrame
    data_to_insert.rename(columns={'GSM_ID':Gsm.platform_.name}, inplace = True)
    data_to_insert['DateTime'] = data_to_insert.index
    ### Write into the database
    data_to_insert = json.loads(data_to_insert.to_json(orient='records',date_format='iso'))

    ##### Build block insert statement and returning ID of new created stations #####
    if len(data_to_insert) != 0 :
        stmt = Gsm.__table__.insert().values(data_to_insert)
        result = DBSession.execute(stmt)
    #     result = list(map(lambda y: y[0], res))
    # else : 
    #     result = []
    # data_to_insert.to_sql(Gsm.__table__.name, DBSession.get_bind(), if_exists='append')
    return res

def get_eng_toInsert(file_obj) :
    file = file_obj.file
    filename=file_obj.filename
    eng_pattern = re.compile('[0]*(?P<platform>[0-9]+)e')
    platform = int(eng_pattern.search(filename).group('platform'))
    # Load raw csv data
    csv_data = pd.read_csv(file, sep='\t',
        index_col=0,
        parse_dates=True,
    )
    # Remove the lines containing NaN
    csv_data.dropna(inplace=True)
    return insert_ENG(platform, csv_data)

def get_ALL_eng_toInsert(file_obj) : 
    file = file_obj.file
    # Load raw csv data
    csv_data = pd.read_csv(file, sep='\t',
        index_col=0,
        parse_dates=True,
    )
    # Remove the lines containing NaN
    csv_data.dropna(inplace=True)
    csv_data.drop(['file_date'], axis=1, inplace=True)
    # get list of ptt
    platform_df = csv_data[['GSM_ID']]
    platform_df = platform_df.groupby('GSM_ID')['GSM_ID'].agg(['count'])
    platform_list = platform_df.index.get_values().tolist()             
    #go to insert data in the database
    return insert_ENG(platform_list, csv_data)

def insert_ENG(platform, csv_data):
    if (type(platform) is list) :
        query = select([GsmEngineering.date]).where(GsmEngineering.platform_.in_(platform))
    elif (type(platform) is int) :
        query = select([GsmEngineering.date]).where(GsmEngineering.platform_== platform)
    else : return 'error type : "platform" '

    '''# Read dates that are already in the database'''
    df = pd.DataFrame.from_records(DBSession.execute(query).fetchall(), index=GsmEngineering.date.name, columns=[GsmEngineering.date.name])
        
    data_to_insert = csv_data[~csv_data.index.isin(df.index)]
    # Rename columns and Date index
    # data_to_insert.rename(columns = {'Temperature_C':'TArE_TEMP','BatteryVoltage_V':'TArE_BATT','ActivityCount':'TArE_TX_CNT'}, inplace=True)       
    # data_to_insert.index.rename('TArE_TXDATE', inplace = True)
    # Add the platform to the DataFrame
    if (type(platform) is int) :
        data_to_insert[GsmEngineering.platform_.name] = platform
        res = {'new Engineering data inserted' : data_to_insert.shape[0]}
    else :
        data_to_insert.rename(columns = {'GSM_ID':GsmEngineering.platform_.name}, inplace = True)
        if (data_to_insert.shape[0] != 0) :
            platform_count = data_to_insert.groupby(GsmEngineering.platform_.name)[GsmEngineering.platform_.name].agg(['count'])
            res = platform_count.to_dict()
            res = {'new Engineering data inserted': res['count']}
        else : 
            res = {'new Engineering data inserted' : 0}
    data_to_insert[GsmEngineering.file_date.name] = datetime.datetime.now()
    print (data_to_insert.columns)
    # Write into the database
    data_to_insert.to_sql(GsmEngineering.__table__.name, DBSession.get_bind(), if_exists='append')
    return res

@view_config(route_name=prefix + 'details', renderer='json')
def indiv_details(request):
    ptt = int(request.matchdict['id'])
    ind_id = int(request.matchdict['ind_id'])
    join_table = join(Individual,V_dataGSM_withIndivEquip, Individual.id == V_dataGSM_withIndivEquip.ind_id) 

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
        V_dataGSM_withIndivEquip.begin_date,
        V_dataGSM_withIndivEquip.end_date]).select_from(join_table).where(and_(V_dataGSM_withIndivEquip.ptt == ptt,V_dataGSM_withIndivEquip.ind_id == ind_id)
                                                              ).order_by(desc(V_dataGSM_withIndivEquip.begin_date))
    data = DBSession.execute(query).first()
    transaction.commit()
    result = dict([ (key[0],key[1]) for key in data.items()])
    query = select([V_Individuals_LatLonDate.c.date]).where(V_Individuals_LatLonDate.c.ind_id == result['ind_id']).order_by(desc(V_Individuals_LatLonDate.c.date)).limit(1)  
    lastObs = DBSession.execute(query).fetchone()
    result['last_observation'] = lastObs['date'].strftime('%d/%m/%Y')
    result['ptt'] = ptt
    return result
