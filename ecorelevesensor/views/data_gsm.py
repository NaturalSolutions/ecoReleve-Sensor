"""
Created on Tue Sep 23 17:15:47 2014
@author: Natural Solutions (Thomas)
"""

from pyramid.view import view_config
from sqlalchemy import desc, select, func, insert, join, Integer, cast, and_, Float, or_
from ecorelevesensor.models import AnimalLocation,ProtocolIndividualEquipment, DBSession, DataGsm, SatTrx, ObjectsCaracValues, Individual,V_Individuals_LatLonDate
from ecorelevesensor.utils.distance import haversine

import pandas as pd
import numpy as np
import re
import datetime,transaction,json

prefix = 'dataGsm/'

@view_config(route_name=prefix + 'unchecked/list', renderer='json')
def data_gsm_unchecked_list(request):
    '''List unchecked GSM data.
    '''
    unchecked = select([
        DataGsm.platform_,
        DataGsm.date
    ]).alias()


    print (unchecked)

    pie = ProtocolIndividualEquipment
    unchecked_with_ind = select([
        pie.ind_id.label('ind_id'),
        unchecked.c.platform_,
        func.count().label('nb')
    ]).select_from(
        unchecked.join(SatTrx, SatTrx.ptt == unchecked.c.platform_)
        .outerjoin(
            pie,
            and_(SatTrx.id == pie.sat_id,
                 unchecked.c['DateTime'] >= pie.begin_date,
                 or_(
                     unchecked.c['DateTime'] < pie.end_date,
                     pie.end_date == None
                )
            )
        )
    ).group_by(unchecked.c.platform_, pie.ind_id).order_by(unchecked.c.platform_)
    # Populate Json array
    data = DBSession.execute(unchecked_with_ind).fetchall()
    return [dict(row) for row in data]

@view_config(route_name=prefix + 'unchecked', renderer='json')
def data_gsm_unchecked(request):
    '''Get the unchecked GSM data.
    '''
    platform = int(request.matchdict['id'])
    
    if request.GET['format'] == 'geojson':
        # Query
        query = select([
            DataGsm.id.label('id'),
            DataGsm.lat,
            DataGsm.lon,
            DataGsm.date
        ]).where(DataGsm.platform_ == platform).where(DataGsm.checked == False
        ).order_by(desc(DataGsm.date)).limit(1000)
        # Create list of features from query result
        features = [
            {
                'type':'Feature',
                'properties':{'date':str(date)},
                'geometry':{'type':'Point', 'coordinates':[float(lon),float(lat)]},
                'id':id_
            }
        for id_, lat, lon, date in DBSession.execute(query).fetchall()]
        transaction.commit()
        result = {'type':'FeatureCollection', 'features':features}
        return result
        
    elif request.GET['format'] == 'json':
        # Query
        query = select([
            DataGsm.id.label('id'),
            DataGsm.lat.label('lat'),
            DataGsm.lon.label('lon'),
            DataGsm.ele.label('ele'),
            DataGsm.date.label('date')]
        ).where(DataGsm.platform_ == platform
        ).where(DataGsm.checked == False
        ).order_by(desc(DataGsm.date)).limit(1000)
        data = DBSession.execute(query).fetchall()
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
        
@view_config(route_name=prefix + 'unchecked/import', renderer='json')
def data_gsm_unchecked_import(request):
    '''Import unchecked GSM data.
    '''
    ptt=request.matchdict['id']
    data = list(request.params)
    print(data)
    data=json.loads(data[0]).get('data')
    id_ind=json.loads(data[0]).get('id_ind')
    select_stmt = DBSession.execute(select([DataGsm],DataGsm.id.in_(data))).fetchall()
    query = insert(AnimalLocation, select_stmt)
    DBSession.execute(query)
    # query = select([
    #     DataGsm.platform_,
    #     func.count(DataGsm.id).label('nb')
    # ]).group_by(DataGsm.platform_)
    
    # return [dict(row) for row in DBSession.execute(query).fetchall()]
    
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
        response = 'An error occured.'
        request.response.status_code = 500
    return response

@view_config(route_name=prefix + 'details', renderer='json')
def indiv_details(request):

    params=int(request.matchdict['id'])
    join_table = join(SatTrx, ObjectsCaracValues, SatTrx.ptt == cast(ObjectsCaracValues.value, Integer)
        ).join(Individual, ObjectsCaracValues.object==Individual.id) 

    query=select([ObjectsCaracValues.value.label('id'), Individual.id.label('ind_id'),Individual.survey_type.label('survey_type'), Individual.status.label('status')
        , Individual.monitoring_status.label('monitoring_status'), Individual.birth_date.label('birth_date'), Individual.ptt.label('ptt'),ObjectsCaracValues.begin_date.label('begin_date'),ObjectsCaracValues.end_date.label('end_date')]
        ).select_from(join_table
        ).where(and_(SatTrx.model.like('GSM%'),ObjectsCaracValues.carac_type==19,ObjectsCaracValues.object_type=='Individual')
        ).where(ObjectsCaracValues.value==params).order_by(desc(ObjectsCaracValues.begin_date))
   
    data=DBSession.execute(query).first()
    transaction.commit()
    if data['end_date'] == None :
        end_date=datetime.datetime.now()
    else :
        end_date=data['end_date'] 

    result=dict([ (key[0],key[1]) for key in data.items()])
    print(result)
    result['duration']=(end_date.month-data['begin_date'].month)+(end_date.year-data['begin_date'].year)*12
    
    query = select([V_Individuals_LatLonDate.c.date]
                     ).where(V_Individuals_LatLonDate.c.ind_id == result['ind_id']
                     ).order_by(desc(V_Individuals_LatLonDate.c.date)).limit(1)
     
    lastObs=DBSession.execute(query).fetchone()
    result['last_observation']=lastObs['date'].strftime('%d/%m/%Y')
    if result['birth_date']!= None:
        result['birth_date']=result['birth_date'].strftime('%d/%m/%Y')
    del result['begin_date'], result['end_date']
    print (result)
    return result
